import json
import requests
import re
import os
import shutil

class Hero(object):
    def __init__(self, hero):
        self.hero = hero
        self.hero_name = hero['data']['name']
        self.path = f'./hero/{self.hero_name}'

    def remove_necessary_char(self, text):
        result = re.sub("#", "", text)
        result = result.replace("\\", "")

        return result

    def download_hero_img(self, url):
        re = requests.get(url)
        hero_url = json.loads(re.text)
        url = hero_url['data'][0]['picture']

        re = requests.get(url, stream=True)

        with open(f"{self.path}/cover.png" , 'wb') as f:
            re.raw.decode_content = True
            shutil.copyfileobj(re.raw, f)


    def create_hero(self):
        story = self.remove_necessary_char(self.hero['data']['des'])
        
        data = {
            'name': self.hero_name,
            'type': self.hero['data']['type'],
            'story': story,
            'status': {
                'durability': self.hero['data']['mag'],
                'offense': self.hero['data']['phy'],
                'ability_effect': self.hero['data']['alive'],
                'difficulty': self.hero['data']['diff']
            },
            'skills': {
                'passive': {
                    'name': self.hero['data']['skill']['skill'][-1]['name'],
                    'icon': self.hero['data']['skill']['skill'][-1]['icon'],
                    'tips': self.hero['data']['skill']['skill'][-1]['tips']
                },
                'first_skill': {
                    'name': self.hero['data']['skill']['skill'][0]['name'],
                    'icon': self.hero['data']['skill']['skill'][0]['icon'],
                    'tips': self.hero['data']['skill']['skill'][0]['tips']
                },
                'second_skill': {
                    'name': self.hero['data']['skill']['skill'][1]['name'],
                    'icon': self.hero['data']['skill']['skill'][1]['icon'],
                    'tips': self.hero['data']['skill']['skill'][1]['tips'],
                },
                'ultimate': {
                    'name': self.hero['data']['skill']['skill'][2]['name'],
                    'icon': self.hero['data']['skill']['skill'][2]['icon'],
                    'tips': self.hero['data']['skill']['skill'][2]['tips'],
                }
            }
        }
        try:
            with open(f'{self.path}/{self.hero_name}.json', 'w') as f:
                json.dump(data, f, indent=4)
        except:
            os.makedirs(self.path)
            with open(f'{self.path}/{self.hero_name}.json', 'w') as f:
                json.dump(data, f, indent=4)
