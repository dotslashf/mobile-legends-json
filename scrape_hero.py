import json
import os
import shutil
import requests
from hero import Hero


class ScrapeHero(object):
    def __init__(self):
        self.file = 'list_hero.json'
        self.root_path = './hero'

    def initial_download(self):
        if os.path.isdir(self.root_path):
            print("Dropping existing folder")
            shutil.rmtree(self.root_path)
        else:
            print("Creating initial folder")
            os.makedirs(self.root_path)

        print("Initiating initial download:\n")

    def download_list_heroes(self):
        url = "https://mapi.mobilelegends.com/hero/list"
        re = requests.get(url)
        hero_list = json.loads(re.text)
        hero_list = hero_list['data']
        for hero in hero_list:
            hero['heroid'] = int(hero['heroid'])
            hero.pop('key')

        hero_list = sorted(hero_list, key=lambda i: i['heroid'])
        print(f'Downloaded {len(hero_list)} heroes')

        hero_objects = json.dumps(hero_list, indent=2)
        with open(f'list_hero.json', 'w') as f:
            f.write(hero_objects)

    def run(self):
        with open(self.file) as json_file:
            data = json.load(json_file)

        for i in range(len(data)):
            print(f"Downloading: {data[i]['name']} {i+1}/{len(data)} Hero")
            hero = Hero(
                f"https://mapi.mobilelegends.com/hero/detail?id={i+1}&language=en")
            hero.create_hero()
