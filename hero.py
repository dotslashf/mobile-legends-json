import json
import requests
import re
import os
import csv
from datetime import datetime


class Hero(object):
    def __init__(self, url):
        self.hero_url = url
        self.hero = self.create_json()
        self.hero_name = self.hero['data']['name']
        self.path = f'./hero/{self.hero_name}'
        self.hero_img_url = url.replace("detail", "atlas")

    def create_json(self):
        re = requests.get(self.hero_url)
        hero_json = json.loads(re.text)

        return hero_json

    def remove_necessary_char(self, text):
        result = re.sub("#", "", text)
        result = result.replace("\\", "")

        return result

    def download_hero_img(self):
        re = requests.get(self.hero_img_url)
        hero_url = json.loads(re.text)
        url = hero_url['data']
        status_download = {'success': 0, 'total': len(url)}

        img_list = []
        for i in range((len(url))):
            img_list.append({'img_name': hero_url['data'][i]['title'],
                             'url': hero_url['data'][i]['picture']})

        print(f"Trying to download {len(img_list)} 🖼️")
        for img in img_list:
            try:
                re = requests.get(img['url'], timeout=10)
                try:
                    print(f"Downloading 🖼️: {img['img_name']} / {img['url']}")

                    # with open(f"{self.path}/img/cover_{img['img_name'].lower().replace(' ', '_')}.png", 'wb') as f:
                    #     f.write(re.content)

                    print(f"Success ✔️\n")
                    status_download['success'] += 1
                except:
                    print(
                        f"No img folder found, creating: {self.hero_name} img 📁")
                    os.makedirs(f"{self.path}/img")
                    print(
                        f"Retry downloading 🖼️: {img['img_name']} / {img['url']}")

                    # with open(f"{self.path}/img/cover_{img['img_name'].lower().replace(' ', '_')}.png", 'wb') as f:
                    #     f.write(re.content)

                    print(f"Success ✔️\n")
                    status_download['success'] += 1
            except:
                print(f"Can't get image {img['img_name']}, skipping ❌")
                self.error_log(img['img_name'], img['url'])
                pass

        return status_download

    def download_hero_skills_img(self, skills):
        print(f"Downloading hero skills icon set:")

        for skill in skills:
            try:
                re = requests.get(skills[skill]['icon'], timeout=10)
                try:
                    with open(f"{self.path}/img/skills/{skill}_{skills[skill]['name'].replace(' ', '_').lower()}.png", 'wb') as f:
                        f.write(re.content)
                except:
                    os.makedirs(f"{self.path}/img/skills")
                    with open(f"{self.path}/img/skills/{skill}_{skills[skill]['name'].replace(' ', '').lower()}.png", 'wb') as f:
                        f.write(re.content)

            except:
                self.error_log(skills[skill]['name'], skills[skill]['icon'])
                pass

        print(f"Success downloading hero skills icon set ✔️")

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
                    'icon': f"{self.path}/img/skills/passive_{self.hero['data']['skill']['skill'][-1]['name'].replace(' ', '_').lower()}.png",
                    'desc': self.hero['data']['skill']['skill'][-1]['des'],
                    'tips': self.hero['data']['skill']['skill'][-1]['tips'],
                },
                'first_skill': {
                    'name': self.hero['data']['skill']['skill'][0]['name'],
                    'icon': f"{self.path}/img/skills/first_skill_{self.hero['data']['skill']['skill'][0]['name'].replace(' ', '_').lower()}.png",
                    'desc': self.hero['data']['skill']['skill'][0]['des'],
                    'tips': self.hero['data']['skill']['skill'][0]['tips']
                },
                'second_skill': {
                    'name': self.hero['data']['skill']['skill'][1]['name'],
                    'icon': f"{self.path}/img/skills/second_skill_{self.hero['data']['skill']['skill'][1]['name'].replace(' ', '_').lower()}.png",
                    'desc': self.hero['data']['skill']['skill'][1]['des'],
                    'tips': self.hero['data']['skill']['skill'][1]['tips'],
                },
                'ultimate': {
                    'name': self.hero['data']['skill']['skill'][2]['name'],
                    'icon': f"{self.path}/img/skills/ultimate_{self.hero['data']['skill']['skill'][2]['name'].replace(' ', '_').lower()}.png",
                    'desc': self.hero['data']['skill']['skill'][2]['des'],
                    'tips': self.hero['data']['skill']['skill'][2]['tips'],
                }
            }
        }

        try:
            print(f"Creating: {self.hero_name} 🦸")

            with open(f'{self.path}/{self.hero_name}.json', 'w') as f:
                json.dump(data, f, indent=4)

            print(f"Success ✔️\n")
        except:
            print(f"No {self.hero_name} found, creating: {self.hero_name} 📁")
            os.makedirs(self.path)

            print(f"Retry creating: {self.hero_name} 🦸")

            with open(f'{self.path}/{self.hero_name}.json', 'w') as f:
                json.dump(data, f, indent=4)

            print(f"Success ✔️\n")

        # self.download_hero_skills_img(data['skills'])
        status_download = self.download_hero_img()
        print(
            f"Done creating: {self.hero_name} ✔️ | ({status_download['success']}/{status_download['total']}) 🖼️\n-----------------------------------\n")

    def error_log(self, img_name, img_url):
        time_now = datetime.now()
        data = {}
        data['hero_name'] = self.hero_name
        data['img_error_url'] = img_url
        data['skin_name'] = img_name
        data['time'] = time_now.strftime("%Y-%d-%m, %H:%M:%S")

        with open('error_log.csv', 'a+') as f:
            fields = ['hero_name', 'img_error_url', 'skin_name', 'time']
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writerow(data)
