import os
import shutil
import time

src_path = "C:/Users/{user_name}/AppData/Local/osu!/Songs" # Change this to the SOURCE path of your beatmap folder
dst_path = "F:/osu!/Songs_test" # Change this to the DESTINATION path of your beatmap folder
mode_to_keep = 3 # Change this to copy only beatmapts of this mode (std = 0, taiko = 1, catch = 2, mania = 3)

start_time = time.time()
transfer = False
countFolder = 0
countError = 0

for folder in os.listdir(src_path): # loop all mapsets
    transfer = False
    try:
        print(f"({countFolder}) Looking for \"{folder}\"")
        for file in os.listdir(f"{src_path}/{folder}"): # loop all maps
            if file.endswith(".osu"):
                with open(f"{src_path}/{folder}/{file}", 'r', encoding="utf-8") as f:
                    for line in f: # loop all lines
                        if line.startswith("Mode:"): 
                            if str(mode_to_keep) in line:
                                countFolder += 1
                                print("Copying...", end="")
                                try:
                                    shutil.copytree(f"{src_path}/{folder}", f"{dst_path}/{folder}") # mania mode
                                    print(".. Done")
                                except Exception:
                                    print(".. Error!")
                                    countError += 1
                                    countFolder -= 1
                                transfer = True
                            break
                f.close()
            if transfer: break
    except Exception: pass

print(f"End, {countFolder} folders copied, {countError} error, took {round(time.time() - start_time, 5)} seconds")
