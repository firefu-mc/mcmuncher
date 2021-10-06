# Copy Dimensions

Command to copy dimensions from 1 world to another.

## Usage

Always backup your Minecraft world directories first!

You must either pass a `--source-bedrock` option which will cause the program to
print a list of all saved worlds in your Minecraft directory, and prompt you
to select one; or you must pass a `--source-directory DIRECTORY` option to point
the program at the directory which contains the Minecraft world to use to copy
the dimension(s) from.

You must either pass a `--target-bedrock` option or a
`--target-directory DIRECTORY` option to select the Minecraft world to use to
copy the dimension(s) to.

```
mcmuncher.exe copy-dimensions --source-bedrock --target-bedrock
```

You can copy multiple dimensions at once, by passing the appropriate options.

`--replace-overworld` Delete the Overworld in the target world before copying the Overworld from the source world.

`--merge-overworld` Copy the Overworld from the source world into the target world.

`--replace-nether` Delete the Nether in the target world before copying the Overworld from the source world.

`--merge-nether` Copy the Nether from the source world into the target world.

`--replace-end` Delete the End in the target world before copying the Overworld from the source world.

`--merge-end` Copy the End from the source world into the target world.

The `--replace-X` and `--merge-X` options for a single dimension are mutually exclusive.

To test what would happen without saving the changes to the world directory,
add the `--dryrun` option.

To output more information to help troubleshoot problems, add the `--verbose`
option.

To view help message, run:
```
mcmuncher.exe copy-dimensions --help
```
