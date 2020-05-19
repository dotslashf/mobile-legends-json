from bs4 import BeautifulSoup
import requests
import json
from hero import Hero

# for i in range(9):
#     i += 1

url = f"https://mapi.mobilelegends.com/hero/detail?id=2&language=en"
# url_cover = f"https://mapi.mobilelegends.com/hero/atlas?id=2&language=en"

hero = Hero(url)
hero.create_hero()

