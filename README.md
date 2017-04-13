# pyunyaml

Sorting the yaml include .asset, .unity(unity scene), .prefab.

- Tested on Unity 5.5.
- Currently uncertain whether there has any issues.

## Install

```
> pip install -r ./requirements.txt
```

## How to use

1. Change the Asset Serialization Mode to Force Text. (Edit -> Project setting -> Asset Serialization -> Mode)
2. Backup all file(.asset|.unity|.prefab) what you want to sort.
3. Do it.

```
python unity_yaml_sorter.py your/data/path/
```

!!! WARNING !!!:

This action will replace the source files. Please backup before you do it.