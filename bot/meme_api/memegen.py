import requests
import json
import os
from bot.settings import BASE_DIR, MEME_USERNAME, MEME_PASSWORD


class Meme:
    meme_dir = f"{BASE_DIR}/meme_api/json/meme_list.json"

    def __init__(self):
        self.gen_meme_url = "https://api.imgflip.com/caption_image"
        self.get_memes_url = "https://api.imgflip.com/get_memes"

        with open(self.meme_dir, "r") as m:
            self.meme_dict = json.load(m)["data"]["memes"]

        self.user_name = MEME_USERNAME
        self.password = MEME_PASSWORD

    def generate_meme(self, *, name, text=None):
        PARAMS = {"username": self.user_name, "password": self.password}
        for meme in self.meme_dict:
            if meme["name"].lower() == name.lower():
                PARAMS["template_id"] = meme["id"]
            if text is not None:
                if len(text) <= meme["box_count"]:
                    for count, each in enumerate(text):
                        this_box = "text" + str(count)
                        PARAMS[this_box] = each
                else:
                    return "Too many text entries"

        r = requests.get(url=self.gen_meme_url, params=PARAMS).json()

        if r["success"]:
            return r["data"]["url"]
        else:
            return None

    def get_all_memes(self):
        r = requests.get(url=self.get_memes_url)
        r = r.json()

        if r["success"]:
            print("updating meme list...")

            with open(self.meme_dir, "w") as f:
                json.dump(r, f)
        else:
            print("Failed to update, aborting...")

    def search_meme_list(self, search_words: list):
        final_dict = {}

        for x in self.meme_dict:
            name = x["name"]
            for each in x["name"].split(" "):
                if any(word in each.lower() for word in search_words):
                    final_dict[name] = x["box_count"]

        if len(final_dict) > 0:
            return "\n".join([f'Name: {x}, Text Boxes: {final_dict[x]}' for x in final_dict.keys()][:10])
        else:
            return None