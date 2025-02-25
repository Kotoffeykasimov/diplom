from dbm import error
import sys
import requests
import configparser
from tqdm import tqdm
from pprint import pprint
import json

congig = configparser.ConfigParser()
congig.read('settings.ini')
vkid = int(input('введите VKID'))
vktoken = congig['Tokens']['vktoken']
yatoken  = congig['Tokens']['yatoken']
folder = input('введите название папки на яндекс диске: ')
qty = int(input('введите количество скачиваемых фото: '))


class VK :
    url = 'https://api.vk.com/method/'


    def __init__(self, id, token):
        self.vkid = id
        self.vktoken = token

    def getphoto(self,qty):
        self.qty = qty
        self.params ={
           'access_token': self.vktoken,
           'owner_id': vkid,
            'v': '5.199',
            'album_id': 'wall',
            'photo_sizes': '1',
            'extended' : 1
        }
        try:
            response = requests.get(f'{self.url}/photos.get',params = self.params).json()
            #print(response)
            photos = response['response']['items']
           #  print(response)

            return photos
        except KeyError:
            print('Неверный VKID или TOKEN , проверьте пожалуйста корректность ввода')
        


class YaDisk:

    def __init__(self,yatoken):
        self.yatoken = yatoken
    def add_folder(self,folder):
        self.folder = folder
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Authorization':  self.yatoken}
        params = {'path': folder}

        response = requests.put(url, headers=headers, params=params)
        #print(response.status_code)

    def savephoto_url(self,urlphoto,folder):
        self.folder = folder
        url ='https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Authorization': self.yatoken}
        params = {
            'path' : folder ,
            'url': urlphoto
        }
        response = requests.post(url, headers=headers, params=params)


def processing_photo():
    likes_list =[]
    final_list = []
    photo = vk.getphoto(qty)
    try:
        for i in tqdm(range(qty)):

            max_photo = max(photo[i]['sizes'],key = lambda x:x['height'])     # максимальный размер по ширине
            #print(max_photo)
            urlphoto = (max_photo['url'])
            likes = photo[i]['likes']['count']
            if likes in likes_list:   # проверка на одинаковое количество лайков
                 likes = f'{likes}({i})'
            ya.savephoto_url(urlphoto, f'{folder}/{likes}.jpg')
            likes_list.append(likes)

            finaldict = {"file_name":f'{likes}.jpg',
                         'size':max_photo['type']
        }
            final_list.append(finaldict)
        print(f'загрузка {qty} файлов в папку {folder} завершена успешно')

    except IndexError:
        pass
    except TypeError:
        pass

#print(final_list)
    final = json.dumps(final_list)
    with open('result.json','w') as f:
        f.write(final)
ya = YaDisk(yatoken)
vk = VK(vkid, vktoken)
ya.add_folder(folder)
processing_photo()














