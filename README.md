#Subroutines
## [Translated from yossy11](https://github.com/yossy11/Subroutines/tree/eefc1ac126ab8bbcfdc62f85844f5fecfd151cb2)

UMAT using Abaqus repository to develop subroutines for

## Folder tree

<pre>
├─Datas Folder for storing various parameters
├─Images Folder for saving images created with matplotlib and various images
├─src_fortran Folder containing fortran77 files
└─src_python Folder containing python files
</pre>

### Files other than the above

- [.devcontainer.json](.devcontainer.json)
  Configuration file for remote-container, a vscode extension. Describes container settings.
- [setup.cfg]
  A file that describes the settings of the python environment. Currently, only formatter and linter settings are described.

## Build Python environment

1. Install Docker, docker-compose
1. Install vscode extension `ms-vscode-remote.remote-containers`
1. Press >< at the bottom left of the screen and select `Remote-Containers: Open Folder in Container`

It takes a long time to create the container for the first time. When the progress bar displayed at the bottom right ends, the environment construction is completed.

## src_python folder

- [draw.py](src_python/draw.py)
  It describes the process of drawing the surrender phase. Use matplotlib's contour method.
- [identify_hill48_params.py](src_python/identify_hill48_params.py),
  [identify_yld2004_params.py](src_python/identify_yld2004_params.py)
  Describe the process to calculate the anisotropic parameters used in each yield function, and to calculate the yield stress and r value in each direction. The calculation of each direction is based on the appendix of [Barlat's paper on his yld2004-18p] (https://www.sciencedirect.com/science/article/abs/pii/S0749641904001160).
- Other files
  It doesn't make much sense to just leave it alone.

## src_fortran folder

- [BaseSubroutine.for](src_fortran/BaseSubroutine.for)
  base subroutine for creating subroutines
- [HardeningRules.for](src_fortran/HardeningRules.for)
  A file describing the hardening law together with its derivative. Please copy accordingly when creating a subroutine.
- [Lib.for](src_fortran/Lib.for)
  A function that is convenient for performing numerical calculations
- [test.for](src_fortran/test.for)
  Prepared to check the behavior of fortran77. There is also a Makefile for compiling this. how to use
  1. Install gfortran
  1. Write test.for appropriately
  1. Hit `make` command
  1. If no error occurs, an executable file will be created under the Debug folder
- [TestSubroutine.for](src_fortran/TestSubroutine.for)
  Prepared to check if subroutine can work with Abaqus. you don't need to use it.
- [YieldFunctions.for](src_fortran/YieldFunctions.for)
  A description of the yield function and its first and second derivatives. Please copy accordingly when creating a subroutine.
- [Yld2004Yld2004Swift.for](src_fortran/Yld2004Yld2004Swift.for)
  A subroutine that implements Yld2004-18P based on the unrelated flow rule

## ABAQUS documentation

http://130.149.89.49:2080/v2016/index.html
