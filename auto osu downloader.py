import os
import sys
import requests as rq
import re
from tqdm import tqdm


#-------------------------------------------------------------------------------------------------------------------------
#######################################################  SETTINGS ########################################################

OSU_MODE = 3 # Change this to copy only beatmaps of this mode (std = 0, taiko = 1, catch = 2, mania = 3)
OSU_PATH = "C:/Users/USERNAME/AppData/Local/osu!/Songs" # Set here your osu songs folder path
MAP_APPROVING = "ranked" # any, ranked, qualified, loved, favourites, pending, graveyard
MAP_DIFFICULTY = (3.4, None) # (Min, Max) stars difficulties at least one map should be between. Put None for unspecified
MANIA_KEYS_AMOUT = 4 # Keys amount for mania maps
DOWNLOAD_VIDEO = False # Change this to True or False if you want to download the video of the maps if any

# Put here your osu creditentials, to be able to download the maps
LOGIN = "USERNAME"
PASSWORD = "PASSWORD"

#-------------------------------------------------------------------------------------------------------------------------

OSU_URL = "https://osu.ppy.sh/home"
OSU_SESSION_URL = "https://osu.ppy.sh/session"
OSU_SEARCH_URL = "https://osu.ppy.sh/beatmapsets/search"
MODES = ["osu", "taiko", "fruits", "mania"]

def formatString(word, forbiden_list, char):
    for c in forbiden_list:
        word = word.replace(c, char)
    return word

def isMapFittingRequirements(beatmap):
    dif_validity = False
    key_amount = False
    dif_min, dif_max = MAP_DIFFICULTY
    if dif_min is None: dif_min = -1
    if dif_max is None: dif_max = 100
    for m in beatmap:
        if m['mode'] != MODES[OSU_MODE]: continue
        if dif_min <= m['difficulty_rating'] <= dif_max: 
            dif_validity = True
            if OSU_MODE == 3 and m['cs'] == MANIA_KEYS_AMOUT: key_amount = True
        
    return dif_validity and (OSU_MODE == 3 and key_amount)

def saveMap(map_id, author, name, data):
    forbiden_char = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    author = formatString(author, forbiden_char, '_')
    name   = formatString(name,   forbiden_char, '_')
    file_path = f"{OSU_PATH}/{map_id} {author} - {name}.osz"
    with open(file_path, "wb") as outfile:
        outfile.write(data)
        
        
def get_token(session):
    homepage = session.get(OSU_URL)
    regex = re.compile(r".*?csrf-token.*?content=\"(.*?)\">", re.DOTALL)
    match = regex.match(homepage.text)
    csrf_token = match.group(1)
    return csrf_token

def connect(session):
    print("Login in...", end=" ")
    data = {"username": LOGIN, "password": PASSWORD, "_token": get_token(session)}
    headers = {"referer": OSU_URL}
    res = session.post(OSU_SESSION_URL, data=data, headers=headers)
    if res.status_code != rq.codes.ok:
        print("✗ Login failed")
        sys.exit(1)
    print("✓ Login successful")

def download(session):
    print("Downloading maps...")
    failed = 0
    skipped = 0
    treated = []
    possessed = []
    for f in os.listdir(OSU_PATH):
        try: possessed.append(int(f.split(" ")[0]))
        except ValueError: continue
    
    headers = {"referer": OSU_SEARCH_URL, "accept": "application/json"}
    maps = session.get(f"{OSU_SEARCH_URL}?m={OSU_MODE}&s={MAP_APPROVING}", headers=headers).json()['beatmapsets']
    for beatmap in tqdm(maps):
        map_id = beatmap["id"]
        
        # mapset already downloaded
        # or map already in folder
        # or map don't fit the requirements
        if map_id in treated or \
           map_id in possessed or \
           not isMapFittingRequirements(beatmap['beatmaps']):
            skipped += 1
            continue 
        treated.append(map_id)
        
        link = f"https://osu.ppy.sh/beatmapsets/{map_id}"
        headers = {"referer": link}
        response = session.get(f"{link}/download?noVideo={str(int(DOWNLOAD_VIDEO))}", headers=headers)
        
        if response.status_code == rq.codes.ok: saveMap(map_id, beatmap['artist'], beatmap['title'], response.content)
        else:
            failed += 1
            continue
    
    print(f"Done, {len(maps) - (failed + skipped)} saved, {failed} failed, {skipped} skipped")
            

def start():
    session = rq.Session()
    connect(session)
    download(session)

    
if __name__ == "__main__":
    start()