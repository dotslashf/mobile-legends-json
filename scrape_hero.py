import json
from hero import Hero


class ScrapeHero(object):
    def __init__(self, file): 
        self.file = file

    def run(self):
        with open(self.file) as json_file:
            data = json.load(json_file)

        for i in range(len(data)):
            hero = Hero(f"https://mapi.mobilelegends.com/hero/detail?id={i+1}&language=en")
            hero.create_hero()

