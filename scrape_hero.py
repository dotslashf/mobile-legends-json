import json
import os
import shutil
from hero import Hero

class ScrapeHero(object):
    def __init__(self, file): 
        self.file = file
        self.root_path = './hero'

    def initial_download(self):
        if os.path.isdir(self.root_path):
            print("Dropping existing folder")
            shutil.rmtree(self.root_path)
        else:
            print("Creating initial folder")
            os.makedirs(self.root_path)

        print("Initiating initial download:\n")

    def run(self):
        with open(self.file) as json_file:
            data = json.load(json_file)

        for i in range(len(data)):
            print(f"Downloading: {data[i]['name']} {i+1}/{len(data)} Hero")
            hero = Hero(f"https://mapi.mobilelegends.com/hero/detail?id={i+1}&language=en")
            hero.create_hero()

