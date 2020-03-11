# Specific gamemode copy
If you want to copy all your osu beatmaps, but in only one gamemode

You'll need to change :
- Line 9 `src_path`, to your `Songs` osu! folder (by default `C:/Users/{user_name}/AppData/Local/osu!/Songs`)
- Line 10 `dst_path`, to where you want your beatmaps to be (for example `F:/osu!/Songs`)
- Line 11 `mode_to_keep`, the gamemode you want to copy (std = 0, taiko = 1, catch = 2, mania = 3)

This works with Python 3.6 or greater, and uses :
- `os` (to iterate all your map)
- `shutil` (to copy the folders)
- `time` (to know the time take by the program to end copying)
