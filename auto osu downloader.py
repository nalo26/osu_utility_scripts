import os

import dotenv
import requests as rq
from tqdm import tqdm

dotenv.load_dotenv()

OSU_MODE = int(os.getenv("OSU_MODE"))
OSU_PATH = os.getenv("OSU_PATH")
MAP_APPROVING = os.getenv("MAP_APPROVING")
MIN_MAP_DIFFICULTY = float(os.getenv("MIN_MAP_DIFFICULTY"))
MAX_MAP_DIFFICULTY = float(os.getenv("MAX_MAP_DIFFICULTY"))
MAP_DIFFICULTY = (MIN_MAP_DIFFICULTY, 100 if MAX_MAP_DIFFICULTY == -1 else MAX_MAP_DIFFICULTY)
MANIA_KEYS_AMOUT = int(os.getenv("MANIA_KEYS_AMOUT"))
DOWNLOAD_VIDEO = bool(int(os.getenv("DOWNLOAD_VIDEO")))

SEARCH_URL = "https://osu.ppy.sh/beatmapsets/search"
MODES = ["osu", "taiko", "fruits", "mania"]


def formatString(word: str, forbiden_list: list[str], char: str) -> str:
    for c in forbiden_list:
        word = word.replace(c, char)
    return word


def isMapFittingRequirements(beatmap) -> bool:
    dif_validity = False
    key_amount = False
    dif_min, dif_max = MAP_DIFFICULTY
    for m in beatmap:
        if m["mode"] != MODES[OSU_MODE]:
            continue
        if dif_min <= m["difficulty_rating"] <= dif_max:
            dif_validity = True
            if OSU_MODE == 3 and m["cs"] == MANIA_KEYS_AMOUT:
                key_amount = True

    return dif_validity and ((OSU_MODE == 3 and key_amount) or OSU_MODE != 3)


def saveMap(session: rq.Session, map_id: int, author: str, name: str):
    forbiden_char = ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]
    author = formatString(author, forbiden_char, "_")
    name = formatString(name, forbiden_char, "_")
    file_path = f"{OSU_PATH}/{map_id} {author} - {name}.osz"
    link = f"https://osu.ppy.sh/beatmapsets/{map_id}"
    headers = {"referer": link}
    response = session.get(f"{link}/download?noVideo={str(int(not DOWNLOAD_VIDEO))}", headers=headers, stream=True)
    total = int(response.headers.get("content-length", 0))

    with open(file_path, "wb") as file, tqdm(
        desc=str(map_id),
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as progress:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress.update(size)


def connect(session: rq.Session):
    print("Enter you osu_session cookie value:")
    input_cookie = input("> ")
    session.cookies.set("osu_session", input_cookie)


def download_all(session: rq.Session):
    print("Downloading maps...")
    failed = 0
    skipped = 0
    treated = []
    possessed = []
    for f in os.listdir(OSU_PATH):
        try:
            possessed.append(int(f.split(" ")[0]))
        except ValueError:
            continue

    headers = {"referer": SEARCH_URL, "accept": "application/json"}
    maps = session.get(f"{SEARCH_URL}?m={OSU_MODE}&s={MAP_APPROVING}", headers=headers).json()["beatmapsets"]
    for beatmap in maps:
        map_id = beatmap["id"]

        # mapset already downloaded OR map already in folder OR map don't fit the requirements
        if map_id in treated or map_id in possessed or not isMapFittingRequirements(beatmap["beatmaps"]):
            skipped += 1
            continue
        treated.append(map_id)
        try:
            saveMap(session, map_id, beatmap["artist"], beatmap["title"])
        except Exception:
            failed += 1

    print(f"Done, {len(maps) - (failed + skipped)} saved, {failed} failed, {skipped} skipped")


if __name__ == "__main__":
    with rq.Session() as session:
        connect(session)
        download_all(session)
