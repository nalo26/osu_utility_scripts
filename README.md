# Auto map downloader (`auto_osu_downloader.py`)
To allow you to download up to the 50 most recent mapsets you don't already have.

**Please copy the `.env.example` to `.env` file to adjust your settings**

This works with Python 3.6 or greater, and uses :
- `dotenv` (to load the settings from the `.env` file)
- `requests` (to download the beatmaps from the osu website)
- `tqdm` (to print a progress bar and estimated time)

*Install the packages with `pip install -r requirements.txt*

To run it, simply execute `python "auto_osu_downloader.py"` in a command shell.


# Specific gamemode copy (`osu transfert.py`)
If you want to copy all your osu beatmaps, but in one specific gamemode

You'll need to change:
- Line 5 `src_path`, to your `Songs` osu! folder (by default `C:/Users/{user_name}/AppData/Local/osu!/Songs`)
- Line 6 `dst_path`, to where you want your beatmaps to be (for example `F:/osu!/Songs`)
- Line 7 `mode_to_keep`, the gamemode you want to copy (std = 0, taiko = 1, catch = 2, mania = 3)

This works with Python 3.6 or greater, and uses :
- `os` (to iterate all your map)
- `shutil` (to copy the folders)
- `tqdm` (to print a progress bar and estimated time)  
*if any of the above is missing, type "`pip install` + package" on a cmd to install it.*

To run it, simply execute `python "osu tranfer.py"` in a command shell.
