#!/usr/bin/env python3
"""Assemble SimCity 4 .dat (DBPF) packages from the text sources in this repository.

Every entry is a file with a matching ``.TGI`` file (Type, Group, Instance on three lines):

* ``*.txt`` with an ``EQZT1###`` header -> binary exemplar / cohort (``EQZB1###`` / ``CQZB1###``)
* ``*.txt`` with type 0x2026960B        -> LTEXT (UTF-16)
* any other file                        -> copied as-is (e.g. ``.lua``)

Usage
-----
    python tools/build_dat.py                         # build every package into ./build
    python tools/build_dat.py "CAM_Controller/CAM_Main_Controller"
    python tools/build_dat.py SRC_DIR -o out/My.dat   # build one .dat to a given path

With no ``-o`` a package folder ``<Package>/<Name>`` is written to
``build/<Package>/a_CAM/0 CAM Controller/<Name>.dat``, ready to copy into the Plugins folder.

Requires Python 3.8+ and no third-party modules.
"""
import argparse
import os
import re
import struct
import sys
import time

TYPE_LTEXT = 0x2026960B
TYPE_EXEMPLAR = 0x6534284A
TYPE_COHORT = 0x05342861

# text type name -> (binary value type, struct format)
VALUE_TYPES = {
    "uint8": (0x01, "B"), "uint16": (0x02, "H"), "uint32": (0x03, "I"),
    "sint32": (0x07, "I"), "sint64": (0x08, "Q"), "float32": (0x09, "f"),
    "bool": (0x0B, "B"), "string": (0x0C, None),
}
MASKS = {"B": 0xFF, "H": 0xFFFF, "I": 0xFFFFFFFF, "Q": 0xFFFFFFFFFFFFFFFF}

PROP_RE = re.compile(r'^(0x[0-9A-Fa-f]{1,8})\s*:\s*\{"(.*?)"\}\s*=\s*(\w+)\s*:\s*(\d+)\s*:\s*\{(.*)\}\s*$')


class BuildError(Exception):
    pass


def parse_int(text):
    value = int(text.strip(), 0)
    return value


def encode_exemplar(text, where):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines or lines[0][:4] not in ("EQZT", "CQZT"):
        raise BuildError(f"{where}: missing EQZT1### / CQZT1### header")
    kind = lines[0][0]  # 'E' exemplar, 'C' cohort
    parent = [0, 0, 0]
    declared = None
    props = []
    for n, line in enumerate(lines[1:], start=2):
        if line.startswith("ParentCohort"):
            parent = [parse_int(x) for x in re.findall(r"0x[0-9A-Fa-f]+", line)]
            if len(parent) != 3:
                raise BuildError(f"{where}:{n}: ParentCohort needs 3 values")
            continue
        if line.startswith("PropCount"):
            declared = parse_int(line.split("=", 1)[1])
            continue
        m = PROP_RE.match(line)
        if not m:
            raise BuildError(f"{where}:{n}: cannot parse line: {line}")
        pid, _name, tname, reps, body = m.groups()
        tkey = tname.lower()
        if tkey not in VALUE_TYPES:
            raise BuildError(f"{where}:{n}: unknown value type {tname}")
        vt, fmt = VALUE_TYPES[tkey]
        out = struct.pack("<I", parse_int(pid)) + struct.pack(">H", vt)
        reps = int(reps)
        if fmt is None:  # string: always stored as a list of characters
            s = body.strip()
            if len(s) < 2 or s[0] != '"' or s[-1] != '"':
                raise BuildError(f"{where}:{n}: string value must be quoted")
            raw = s[1:-1].encode("latin-1")
            out += b"\x80\x00\x00" + struct.pack("<I", len(raw)) + raw
        else:
            items = [v.strip() for v in body.split(",")] if body.strip() else []
            vals = []
            for v in items:
                if tkey == "float32":
                    vals.append(float(v))
                elif tkey == "bool":
                    vals.append(1 if v.lower() in ("true", "1", "0x01") else 0)
                else:
                    vals.append(parse_int(v) & MASKS[fmt])
            if reps == 0:
                if len(vals) != 1:
                    raise BuildError(f"{where}:{n}: Reps 0 requires exactly one value")
                out += b"\x00\x00\x00"
            else:
                if len(vals) != reps:
                    raise BuildError(f"{where}:{n}: Reps is {reps} but {len(vals)} values given")
                out += b"\x80\x00\x00" + struct.pack("<I", len(vals))
            out += struct.pack("<" + fmt * len(vals), *vals)
        props.append(out)
    if declared is not None and declared != len(props):
        raise BuildError(f"{where}: PropCount is {declared} but {len(props)} properties found")
    head = (kind + "QZB1###").encode("ascii")
    return head + struct.pack("<4I", *parent, len(props)) + b"".join(props)


def encode_ltext(text):
    if text.endswith("\n"):
        text = text[:-1]
    raw = text.encode("utf-16-le")
    return struct.pack("<H", len(raw) // 2) + b"\x00\x10" + raw


def read_tgi(path):
    parts = open(path, encoding="ascii").read().split()
    if len(parts) != 3:
        raise BuildError(f"{path}: expected 3 hex values (Type, Group, Instance)")
    return tuple(int(p, 16) for p in parts)


def collect_entries(src):
    entries = {}
    for root, dirs, files in os.walk(src):
        dirs.sort()
        for f in sorted(files):
            if not f.endswith(".TGI"):
                continue
            tgi_path = os.path.join(root, f)
            data_path = tgi_path[:-4]
            if not os.path.isfile(data_path):
                raise BuildError(f"{tgi_path}: no matching data file")
            tgi = read_tgi(tgi_path)
            if tgi in entries:
                raise BuildError(f"duplicate TGI {tgi_str(tgi)} in {data_path}")
            raw = open(data_path, "rb").read()
            if raw[:4] in (b"EQZT", b"CQZT"):
                data = encode_exemplar(raw.decode("utf-8"), data_path)
            elif tgi[0] == TYPE_LTEXT and data_path.endswith(".txt"):
                data = encode_ltext(raw.decode("utf-8"))
            else:
                data = raw
            entries[tgi] = data
    if not entries:
        raise BuildError(f"{src}: no entries found (no .TGI files)")
    return entries


def tgi_str(tgi):
    return "0x%08X-0x%08X-0x%08X" % tgi


def write_dbpf(entries, out_path):
    """Write an uncompressed DBPF 1.0 package with a 7.0 index (the SC4 format)."""
    now = int(time.time())
    header_size = 96
    body = bytearray()
    index = bytearray()
    for tgi in sorted(entries):
        data = entries[tgi]
        index += struct.pack("<5I", *tgi, header_size + len(body), len(data))
        body += data
    index_offset = header_size + len(body)
    header = struct.pack(
        "<4s2I12x2I8I",
        b"DBPF", 1, 0,          # magic, major, minor
        now, now,               # created, modified
        7, len(entries),        # index major version, entry count
        index_offset, len(index),
        0, 0, 0,                # holes: count, offset, size
        0,                      # index minor version
    )
    header += b"\x00" * (header_size - len(header))
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(header + body + index)


def find_dat_folders(repo):
    """A .dat folder is a folder inside a package folder (<repo>/<Package>/<Name>)."""
    result = []
    for pkg in sorted(os.listdir(repo)):
        pdir = os.path.join(repo, pkg)
        if not os.path.isdir(pdir) or pkg.startswith(".") or pkg in ("tools", "build"):
            continue
        for name in sorted(os.listdir(pdir)):
            if os.path.isdir(os.path.join(pdir, name)):
                result.append((pkg, name))
    return result


def build(src, out_path):
    entries = collect_entries(src)
    write_dbpf(entries, out_path)
    print(f"{out_path}  ({len(entries)} entries)")


def main():
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser(description="Assemble SimCity 4 .dat files from text sources.")
    ap.add_argument("src", nargs="*", help=".dat source folder(s); default: all packages")
    ap.add_argument("-o", "--output", help="output .dat path (only with a single source folder)")
    ap.add_argument("-b", "--build-dir", default=os.path.join(repo, "build"),
                    help="output root when -o is not given (default: ./build)")
    args = ap.parse_args()

    if args.output and len(args.src) != 1:
        ap.error("-o/--output needs exactly one source folder")
    try:
        if args.output:
            build(args.src[0], args.output)
            return 0
        if args.src:
            targets = []
            for s in args.src:
                s = os.path.abspath(s)
                targets.append((os.path.basename(os.path.dirname(s)), os.path.basename(s), s))
        else:
            targets = [(p, n, os.path.join(repo, p, n)) for p, n in find_dat_folders(repo)]
        for pkg, name, src in targets:
            build(src, os.path.join(args.build_dir, pkg, "a_CAM", "0 CAM Controller", name + ".dat"))
    except BuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
