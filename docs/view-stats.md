# View Stats

Command to view various details about a world.

## Usage

You must either pass a `--bedrock` option which will cause the program to
print a list of all saved worlds in your Minecraft directory, and prompt you
to select one; or you must pass a `--directory DIRECTORY` option to point
the program at the directory which contains the Minecraft world.

```
mcmuncher.exe view-stats --bedrock
# OR
mcmuncher.exe view-stats --directory DIRECTORY
```

To view details of the further chunks / coordinates existing in each cardinal
direction, pass the `--extent` option.

```
mcmuncher.exe view-stats --bedrock --extent
```

To view the maximum allow bounds of each dimension, pass the `--bounds` option.
Usually +/-30M for worlds.

```
mcmuncher.exe view-stats --bedrock --bounds
```

To view details on all players in the world, pass the `--players` option.
May output a lot of warnings.

```
mcmuncher.exe view-stats --bedrock --players
```

To view help message, run:
```
mcmuncher.exe view-stats --help
```

## Example output

The command:
```
python mcmuncher.py view-stats --directory DIRECTORY --extent --players
```

Example output:
```
2021-08-26 21:48:50,262 - amulet_core - INFO - Loading level DIRECTORY

level_path: DIRECTORY

Dimensions:
('minecraft:overworld', 'minecraft:the_nether', 'minecraft:the_end')

minecraft:overworld
197 chunks
Chunks span: East(-21), West(52), North(-21), South(58)
Coords span: East(-336), West(847), North(-336), South(943)

minecraft:the_nether
0 chunks

minecraft:the_end
0 chunks

Players:
{'~local_player'}

id: ~local_player
dimension: minecraft:overworld
location: (272.5, 64.62001037597656, 16.5)
rotation: (0.0, 0.0)
```
