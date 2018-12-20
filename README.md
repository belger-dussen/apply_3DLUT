# apply_3DLUT
Apply 3D LUT to image(s) using linear interpolation.

## Dependencies
Tested with folowing version of libraries:
+ Python 2/3

## Usage
### Single Image
```shell
python apply_3DLUT.py PATH/TO/IMAGE PATH/TO/3DLUT.cube
```
### Multiple Images
```shell
python apply_3DLUT.py PATH/TO/IMAGE/DIRECTORY PATH/TO/3DLUT.cube --batch
```