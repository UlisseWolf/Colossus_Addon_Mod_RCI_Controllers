<div align="center">

# Colossus Addon Mod — RCI Controllers

**Readable source of the Colossus Addon Mod (CAM) RCI controller packages for SimCity 4**

[![License: LGPL v2.1](https://img.shields.io/badge/License-LGPL_v2.1-blue.svg)](LICENSE)
[![Game: SimCity 4](https://img.shields.io/badge/Game-SimCity%204-orange.svg)](#requirements)
[![Version: 1.1.641](https://img.shields.io/badge/SC4-1.1.641%20(digital)-green.svg)](#requirements)

</div>

---

## Table of contents

- [About](#about)
- [Packages](#packages)
- [Repository structure](#repository-structure)
- [File format](#file-format)
- [Building a .dat file](#building-a-dat-file)
- [Requirements](#requirements)
- [Installation](#installation)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)

## About

**Colossus Addon Mod (CAM)** is a SimCity 4 mod that substantially changes the RCI (Residential – Commercial – Industrial) simulation and fixes essential bugs in the game.

The RCI controllers are the core of the mod: they define the demand sources, the development stages, the census groups and the simulator tuning that drive how a city grows. This repository stores the content of the controller `.dat` files as **plain text**, so every change can be reviewed, compared and tracked with Git instead of being hidden inside a binary package.

## Packages

Each package is an alternative controller: install **only one** of them.

| Package | Version | `.dat` file(s) | Entries | Description |
|---|:---:|---|:---:|---|
| [CAM Controller](Colossus_Addon_Mod_-_CAM_Controller_V_3.1.1) | 3.1.1 | `CAM_Main_Controller.dat`<br>`CAM_PlayStyle_Extended.dat` | 116<br>13 | The full CAM simulation with extended stages and play styles. |
| [SPAM Controller](Colossus_Addon_Mod_-_SPAM_Controller_V_3.1.0) | 3.1.0 | `CAM_SPAM Controller.dat` | 17 | Updated version of SPAM: fixes agricultural demand without altering the RCI simulation, while keeping the CAM enhancements. |
| [Vanilla Controller](Colossus_Addon_Mod_-_Vanilla_Controller_V3.1.1) | 3.1.1 | `CAM_Vanilla Controller.dat` | 11 | Enhanced vanilla simulation: includes the CAM improvements but keeps the classic Maxis gameplay, without the farm-related changes. |

## Repository structure

Each top-level folder corresponds to one release archive and mirrors its layout. Every `.dat` file is replaced by a folder with the same name, which holds one subfolder per entry type:

```text
Colossus_Addon_Mod_-_<Package>_V<version>/
└── a_CAM/
    └── 0 CAM Controller/
        └── <dat file name>/
            ├── Exemplar/
            │   ├── <Exemplar Name> (0xGROUP-0xINSTANCE).txt
            │   └── <Exemplar Name> (0xGROUP-0xINSTANCE).txt.TGI
            └── LTEXT/
                ├── LTEXT (0xGROUP-0xINSTANCE).txt
                └── LTEXT (0xGROUP-0xINSTANCE).txt.TGI
```

## File format

### Exemplars

Exemplars are stored as SC4 **text exemplars** (`EQZT1###`), the format used by Reader and iLive's Reader:

```text
EQZT1###
ParentCohort=Key:{0x00000000,0x00000000,0x00000000}
PropCount=0x00000009
0x00000010:{"Exemplar Type"}=Uint32:0:{0x00000005}
0x00000020:{"Exemplar Name"}=String:1:{"Fire Protection Simulator"}
0x29233E8F:{"FireProtectionSim, Max Allowed Funding"}=Float32:0:{120}
0x29233E98:{"FireProtectionSim, Strike Response Curve"}=Float32:8:{0,100,25,25,50,10,70,0}
```

Each property line follows the pattern `0xPROPERTYID:{"Name"}=Type:Reps:{values}`, where `Reps` is `0` for a single value and the number of values for a list.

- Property names come from [New_Properties.xml-patches](https://github.com/UlisseWolf/New_Properties.xml-patches).
- All values are written losslessly: converting a text file back to binary gives exactly the original entry, byte for byte.

### LTEXT

LTEXT entries (localized strings) are stored as UTF-8 text.

### TGI files

Next to every entry there is a `.TGI` file with three lines: the **Type**, **Group** and **Instance** IDs of the entry inside the `.dat` package.

```text
6534284A
E7E2C2DB
68F5524A
```

## Building a .dat file

1. Open **Reader** (or **iLive's Reader**) and create a new, empty file.
2. Right-click in the entry list and choose **Import File**.
3. Select an entry `.txt` file and give it the Type, Group and Instance listed in the matching `.TGI` file.
4. Repeat for every entry in the `.dat` folder.
5. Save the package with the original `.dat` name.

## Requirements

> [!WARNING]
> From version 2.5 onward, Colossus Addon Mod works **only with the digital version (1.1.641) of SimCity 4** on Microsoft Windows and Linux. On other systems the mod may malfunction and no support is provided.

| Dependency | Purpose |
|---|---|
| [SC4 System Integration Module (SIM)](https://community.simtropolis.com/files/file/36978-sc4-system-integration-module-sim/) | Essential dependency for CAM |
| [Colossus Addon Mod – Ordinances](https://community.simtropolis.com/files/file/36878-colossus-addon-mod-ordinances/) | Enhances and expands ordinances |

No DLL dependencies are required.

## Installation

1. Build the `.dat` file(s) of the package you want (see [Building a .dat file](#building-a-dat-file)), or download the released archive.
2. Copy the `a_CAM` folder into `Documents\SimCity 4\Plugins` (or your custom Plugins folder).
3. Remove any previous CAM version from your plugins. Using [SC4 Cleanitol](https://community.simtropolis.com/files/file/35790-sc4-cleanitol/) is highly recommended.

> [!IMPORTANT]
> Install only **one** controller package at a time.

## Contributing

Bug reports and suggestions are welcome through [Issues](../../issues). For changes:

1. Fork the repository and create a branch from `staging`.
2. Edit the text exemplars, keeping the `EQZT1###` format and the matching `.TGI` files.
3. Open a pull request that describes what changes in the simulation and why.

## Credits

Colossus Addon Mod is developed by the **CAM Team**. The following SimCity 4 community members contributed models, textures and modding support:

Ulisse Wolf · Tyberius06 · Cyclone Boom · CorinaMarie · InvisiChem · Indisguise · BarbyW · Wouanagaine · JMyers2043 · Shoreman905 · Rayden · MAS71 · Jplumbley · Andreas · Callagrafx · Tropod · RippleJet · Tag one · Memo33 · Dragonsteincole · xBlaze89x · paeng · Pegasus

Packages assembled by **Ulisse Wolf**. Special thanks to the staff of SC4Evermore, Simtropolis and SC4 Devotion, to the SimCity 4 community and to Maxis.

## License

This project is licensed under the **GNU Lesser General Public License v2.1** — see the [LICENSE](LICENSE) file for details.

SimCity 4 is a trademark of Electronic Arts Inc. This project is not affiliated with or endorsed by Electronic Arts or Maxis.
