# Trim Chunks

Command to trim chunks from world dimensions - deleting any chunks you don't want.

## Usage

You must either pass a `--bedrock` option which will cause the program to
print a list of all saved worlds in your Minecraft directory, and prompt you
to select one; or you must pass a `--directory DIRECTORY` option to point
the program at the directory which contains the Minecraft world.

```
mcmuncher.exe trim-chunks --bedrock
# OR
mcmuncher.exe trim-chunks --directory DIRECTORY
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

To trim just the overworld dimension:
```
mcmuncher.exe trim-chunks --bedrock --keep-overworld path\to\overworld-coords.txt
```

To trim all 3 dimensions at once:
```
mcmuncher.exe trim-chunks --bedrock --keep-overworld path\to\overworld-coords.txt --keep-nether path\to\nether-coords.txt --keep-end path\to\end-coords.txt
```

To test what would happen without saving the changes to the world directory,
add the `--dryrun` option.
```
mcmuncher.exe trim-chunks --bedrock --dryrun --keep-overworld path\to\overworld-coords.txt
```

To output more information to help troubleshoot problems, add the `--verbose`
option.
```
mcmuncher.exe trim-chunks --bedrock --verbose --keep-overworld path\to\overworld-coords.txt
```

To view help message, run:
```
mcmuncher.exe trim-chunks --help
```
