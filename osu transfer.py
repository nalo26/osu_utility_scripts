import os
import shutil
from tqdm import tqdm

src_path = "C:/Users/{USER_NAME}/AppData/Local/osu!/Songs" # Change this to the SOURCE path of your beatmap folder
dst_path = "F:/osu!/Songs" # Change this to the DESTINATION path of your beatmap folder
mode_to_keep = 3 # Change this to copy only beatmapts of this mode (std = 0, taiko = 1, catch = 2, mania = 3)

transfer = False
countFolder = 0
countError = 0
countSkip = 0

for folder in tqdm(os.listdir(src_path)): # loop all mapsets
    transfer = False
    try:
        if folder in os.listdir(dst_path): # map altready transfered, skip
            countSkip += 1
            continue
        for file in os.listdir(f"{src_path}/{folder}"): # loop all maps
            if file.endswith(".osu"):
                with open(f"{src_path}/{folder}/{file}", 'r', encoding="utf-8") as f:
                    for line in f: # loop all lines
                        if line.startswith("Mode:"): 
                            if str(mode_to_keep) in line:
                                countFolder += 1
                                try: shutil.copytree(f"{src_path}/{folder}", f"{dst_path}/{folder}") # copy folder
                                except Exception: countError += 1
                                transfer = True
                            break
                f.close()
            if transfer: break
    except Exception: pass

print(f"End, {countFolder} folders copied, {countError} error, {countSkip} skipped (already present)")