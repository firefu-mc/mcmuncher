# Minecraft Muncher

Various programs to edit MineCraft worlds using the Amulet API.

All paths/commands in this documentation are for MS Windows - for other
platforms, change as appropriate.

This has only been tested with Bedrock worlds.

# Included programs

## trim-chunks

Command to trim chunks from world dimensions - deleting any chunks you don't want.

See [docs/trim-chunks.md](docs/trim-chunks.md) for details.

## view-stats

Command to view a report of various details about a world.

See [docs/view-stats.md](docs/view-stats.md) for details.

# Obtaining

You can either download the MS Windows `mcmuncher.exe` program from
[github](https://github.com/firefu-mc/mcmuncher/releases), or you can run the
source python file directly, or build your own `.exe` file from source.

## Running / building from source

[Checkout](https://github.com/firefu-mc/mcmuncher.git)
or
[download](https://github.com/firefu-mc/mcmuncher/archive/refs/heads/master.zip)
the files from github.

## Preparing python environment

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

## Running the python script

```
python mcmuncher COMMAND [--args]
```

## Building the .EXE yourself

```
pip install pyinstaller
venv-mcmuncher\Scripts\pyinstaller.exe --onefile -c -p venv-mcmuncher\Lib\site-packages mcmuncher.py
```

The `mcmuncher.exe` program will be saved to the `dist` directory.

# Developers

To update the dependencies / libraries:
```
pip list
# If any packages are flagged as out of date, run the following,
# replacing NAME as appropriate
python -m pip install --upgrade NAME
```

## Running unit tests

```
python -m unittest
```
