# Colossus Addon Mod - RCI Controllers

Colossus Addon Mod (CAM) is a SimCity 4 mod that changes RCI (Residential - Commercial - Industrial) development, extending gameplay and fixing bugs.

This repository contains the **readable source** of the three CAM RCI controller packages. Every `.dat` file has been unpacked: each entry (exemplar, LTEXT) is stored as a plain-text file, so changes can be reviewed and compared with Git.

## Packages

| Package | Version | `.dat` files |
|---|---|---|
| [CAM Controller](Colossus_Addon_Mod_-_CAM_Controller_V_3.1.1/) | 3.1.1 | [CAM_Main_Controller.dat](Colossus_Addon_Mod_-_CAM_Controller_V_3.1.1/a_CAM/0%20CAM%20Controller/CAM_Main_Controller/INDEX.md), [CAM_PlayStyle_Extended.dat](Colossus_Addon_Mod_-_CAM_Controller_V_3.1.1/a_CAM/0%20CAM%20Controller/CAM_PlayStyle_Extended/INDEX.md) |
| [SPAM Controller](Colossus_Addon_Mod_-_SPAM_Controller_V_3.1.0/) | 3.1.0 | [CAM_SPAM Controller.dat](Colossus_Addon_Mod_-_SPAM_Controller_V_3.1.0/a_CAM/0%20CAM%20Controller/CAM_SPAM%20Controller/INDEX.md) |
| [Vanilla Controller](Colossus_Addon_Mod_-_Vanilla_Controller_V3.1.1/) | 3.1.1 | [CAM_Vanilla Controller.dat](Colossus_Addon_Mod_-_Vanilla_Controller_V3.1.1/a_CAM/0%20CAM%20Controller/CAM_Vanilla%20Controller/INDEX.md) |

## File format

- **Exemplars** are saved as SC4 text exemplars (`EQZT1###`), one property per line:

  ```
  0xPROPERTYID:{"Property Name"}=Type:Reps:{values}
  ```

  `Reps` is `0` for a single value, otherwise the number of values. Property names come from [New_Properties.xml-patches](https://github.com/UlisseWolf/New_Properties.xml-patches). Numbers are written losslessly: converting a text file back to binary gives exactly the original entry.
- **LTEXT** entries are saved as UTF-8 text.
- Next to each file there is a `.TGI` file with three lines: Type, Group and Instance of the entry.
- Every unpacked `.dat` folder contains an `INDEX.md` listing all its entries with their TGI.

## Compiling a .dat file

Create a new empty file in Reader (or iLive's Reader), right-click → *Import File*, select a `.txt` exemplar and set the Type, Group and Instance shown in the matching `.TGI` file. Repeat for every entry, then save the `.dat`.
