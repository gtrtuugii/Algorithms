# Build Instructions:

## General Remarks

This is likely to not work inside a VM/WSL, or atleast is not worth the effort getting it to work,
because it is designed to be built natively on Windows, Linux and Mac.
(Note: A dual boot will work, but is not needed)

As a part of building on any of Windows, Linux and Mac,
you are not restricted to one of those OS once you have started,
you can switch at any point by just deleting the build directory which is generate 
which can be done by `clean`ing the project or manually deleting the generated folder 
which would called `cmake-build…`, `buildDir` or something to that effect and then
just copying the whole project directory over to the other computer.

# Lab PCs

If you wish to use the do the project on the lab PC’s,
then boot them into Linux, place the unzipped project template somewhere on your student drive
so that it’ll be there when you reboot and then open a terminal in the project folder 
so that `ls` will list `src` `res` `lib` etc… .
From here you can then run the commands:

To build the project:
> make

To run the project:
> make run

To clean the project (one of):
> make clean

> make clobber

# Personal PCs

## Some required dependencies (somethings may be missing):

#### Linux:

* (If you could build the labs, the only extra thing you need is cmake.)
* A build chain, like: gcc/g++ or clang, etc
* The build tool: `cmake`
  * A simple `sudo apt install cmake` should work, or whatever is appropriate for your distro

* Some dev dependencies, which for me on a fresh Ubuntu 20.04 VM are: `sudo apt install cmake libxmu-dev g++ libx11-dev libgl1-mesa-dev libglu1-mesa-dev xorg-dev libxi-dev`

#### Mac:

* A build chain, like: gcc/g++ or clang, etc
* The build tool: `cmake`
  * Download `.dmg` mac installer from https://cmake.org/download/ and install
  * Then run the cmake program (like you'd open any other) then from the `Tools` menu select `How to Install For Command Line Use`
    and run one of the options that is presented to you.
  * You can now close cmake
* x11 from https://xquartz.org

#### Windows:

* (If you could build the Windows-Labs Windows port of the labs then you already have everything)
* Visual Studio (not code), and select the `Desktop development with C++` `Workload` in the installer https://visualstudio.microsoft.com/downloads
* The build tool: `cmake`
  * Download `.msi` Windows installer from https://cmake.org/download/
  * When installing, **tick the box that asks you if you want to add it to the PATH.**
    * Should you fail to do this, you must add it manually afterwards

## Initial setup:
* Download the project template .zip file and unzip it somewhere
* Download the assets .zip, unzip that and place the folder called `models-textures` inside the `res` folder in the project

## Building/Running the project:

### CLion:
  Open the top folder which contains the 'CMakeLists.txt', then in the top right edit the start_scene configuration
  set the working directory to `$ProjectFileDir$`.

  _NOTE: On Windows you must use the Visual Studio tool chain:_
        `file` > `settings` > `Build, Execution, Deployment` > `Toolchains`: Add Visual Studio,
        then `Build, Execution, Deployment` > `cmake` make sure `toolchain` is set to Visual Studio for which ever configurations you want to use

### VS Code:
  Open the top folder and I would suggest the `C/C++`, `CMake` and `CMake Tools` extensions.
  Then you build the project with `f7` (or right clicking CMakeLists.txt and selecting `build all`) and when it asks for which build tools to use, select the second option which is to just let it pick.
  Then when you try to run it via Run->Start (Without Debugging) you will need to setup a launch.json, just set
  `"program": "${workspaceFolder}/start_scene"` (On Windows you need to add `.exe`) and it should just work now.
  (see for more on how to use CMake Tools: https://github.com/microsoft/vscode-cmake-tools/blob/main/docs/how-to.md#build-a-project)

### Visual Studio (Windows Only)
  `cd` into the top project folder, so that `ls` should list `CMakeLists.txt`, `src`, `lib`, `res`, etc...
  generate build files: 
  >cmake -S . -B cmake-build

  Then open the `cmake-build` directory and open the `start_scene.sln` file (with Visual Studio) and everything should just work.


### Command line / Other IDE fall back:
  `cd` into the top project folder, so that `ls` should list `CMakeLists.txt`, `src`, `lib`, `res`, etc...
  generate build files:
  > cmake -S . -B cmake-build

  build:
  > cmake --build cmake-build

  run:
  > ./start_scene

  to clean:
  > cmake --build cmake-build-debug --target clean

  Doesn't work on windows:

  build with multiple (e.g. 4) threads:
  > cmake --build cmake-build -- -j 4


# Further notes:
You may find that the scroll wheel does nothing on MacOS, this happens, 
but isn’t a big deal as you can either just drag the mouse up/down, press alt+(w or up) and alt+(s or down) to do the same thing.

# Files Descriptions:

* `Makefile`:
  The makefile used by `make` exclusively when you are building the project on a lab PC

* `CMakeLists.txt`: 
  The CMake file used by `cmake` to generate the build files for you system/toolchain
  
* `.gitignore`: 
  Just some useful things for git to ignore should you should to use git or VCS
  
* `lib` directory: 
  The directory which contains the sources of the libraries used by to build the project, 
  also prebuilt assimp library for use on the lab PCs
  
* `res` directory: 
  The directory which contains the runtime resources used by the program:
  * res/models-textures: 
    The directory which contains the models and textures loaded by the program at runtime
  * res/shaders:
    The directory which contains the shaders loaded by the program at runtime
    
* `src` directory: 
  The directory which contains the main source file you will be editing: `scene-start.cpp`.
  It also contains some other source files you can edit.
  Also should you want to add more .cpp files this is where you would put them
  
## Adding more source files
Should you for whatever reason decide to add more source files (.cpp's) to have them properly added:
* Edit line 19 of `Makefile` so as to add your new source file to the end of the `SRC` definition, e.g.\
  `SRC = src/scene-start.cpp lib/angel/src/InitShader.cpp lib/bitmap/src/bitmap.c` ->\
  `SRC = src/scene-start.cpp lib/angel/src/InitShader.cpp lib/bitmap/src/bitmap.c src/my_source.cpp`

* Edit line 36 of `CMakeLists.txt` so as to add you new source file to the list in `add_executable`, e.g.\
  `add_executable(start_scene src/scene-start.cpp src/gnatidread.h src/gnatidread2.h)` ->\
  `add_executable(start_scene src/scene-start.cpp src/gnatidread.h src/gnatidread2.h src/my_source.cpp)`
  
* Then if not on a lab PC regenerate the project files, either your IDE should handle this
  or like in the case of Visual Studio rerun: `cmake -S . -B cmake-build` and reload the project
