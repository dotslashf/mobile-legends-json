from bs4 import BeautifulSoup
import requests
import json
from hero import Hero

for i in range(10):
    i += 1

    url = f"https://mapi.mobilelegends.com/hero/detail?id={i}&language=en"
    url_cover = f"https://mapi.mobilelegends.com/hero/atlas?id={i}&language=en"

    re = requests.get(url)
    content = re

    hero_json = json.loads(re.text)

    hero = Hero(hero_json)
    hero.create_hero()
    hero.download_hero_img(url_cover)

