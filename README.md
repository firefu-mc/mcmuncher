# Minecraft Muncher

Program to trim Minecraft dimensions - deleting any chunks you don't want.

To just use the `mcmuncher.exe` file download from github,
skip to the `Usage` section below.

All paths/commands in this documentation are for Windows - for other platforms,
change as appropriate.

## Preparing environment

Install Python 3 https://www.python.org/downloads/

Create a virtual Python environment for this project:
```
python -m venv venv-mcmuncher
venv-mcmuncher\Scripts\activate.bat
```

Install python dependencies with:
```
python -m pip install -r requirements.txt
```

## Building the .EXE yourself

```
pip install pyinstaller
venv-mcmuncher\Scripts\pyinstaller.exe --onefile -c -p venv-mcmuncher\Lib\site-packages mcmuncher.py
```

The `mcmuncher.exe` program will be saved to the `dist` directory.

## Usage

Always backup your Minecraft world directory first!

Run the program from a Command Prompt:
```
Start Menu > cmd
```

To run the program, either change your working directory to where you saved
it.
```
cd Downloads
```
Or supply the full path to the program every time you run it:
```
Downloads\mcmuncher.exe --options
```

You must either pass a `--bedrock` option which will cause the program to
print a list of all saved worlds in your Minecraft directory, and prompt you
to select one; or you must pass a `--directory DIRECTORY` option to point
the program at the directory which contains the Minecraft world.

```
mcmuncher.exe --bedrock
# OR
mcmuncher.exe --directory DIRECTORY
```

You can trim multiple dimensions at once, by passing the appropriate options.

You record which chunks to keep for each dimensions in a separate text file.
Any chunks not in that text file will be deleted from the world.

An example of a text file:
```
# Comments start with the "#" character - these are ignored.
# All non-comment lines must contain the coordinates for any 2 opposite
# corners of a rectangle - representing an area to keep.
-1500,1500    1500,1500
# There must be no spaces in each "x,z" coordinate.
# But there must be at least 1 space (and no other characters) between
# the 2 coordinate pairs.
#
# The rectangles can overlap, that's not a problem.
1400,1600    800,1200
```

To see all available options, run:
```
mcmuncher.exe -h
```

To trim just the overworld dimension:
```
mcmuncher.exe --bedrock --keep-overworld path\to\overworld-coords.txt
```

To trim all 3 dimensions at once:
```
mcmuncher.exe --bedrock --keep-overworld path\to\overworld-coords.txt --keep-nether path\to\nether-coords.txt --keep-end path\to\end-coords.txt
```

To test what would happen without saving the changes to the world directory,
add the `--dryrun` option.
