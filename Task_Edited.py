import requests
import os.path
from urllib.parse import urlencode
import json

# OAUTH_URL = 'https://oauth.vk.com/authorize'
# APP_ID = 7540196
#
# OAUTH_DATA = {
#     'client_id': APP_ID,
#     'display': 'mobile',
#     'scope': 'status,audio',
#     'response_type': 'token',
#     'v': 5.120,
#     'redirect_uri': 'https://oauth.vk.com/blank.html'
# }
#
# print('?'.join(
#     (OAUTH_URL, urlencode(OAUTH_DATA))
# ))

class Photo_Uploader():
    def __init__(self, VK_token, id_number, Ya_token, number_of_photos):
       self.VK_token = VK_token
       self.id_number = id_number
       self.Ya_token = Ya_token
       self.number_of_photos = number_of_photos

    def get_photo(self):
        self.response = requests.get(
            'https://api.vk.com/method/photos.get',
            params={
                'owner_id': self.id_number,
                'album_id': 'profile',
                'access_token': self.VK_token,
                'v': '5.120',
                'extended': 1,
            }
        )
        return self.response.json()


    def download_photo(self,):
        photos = self.get_photo()['response']['items']
        last_photos = photos[-(self.number_of_photos):]
        likes = [last_photo['likes']['count'] for last_photo in last_photos]
        max_photos = [last_photo['sizes'][-1] for last_photo in last_photos]
        urls = [max_photo['url'] for max_photo in max_photos]
        sizes = [max_photo['type'] for max_photo in max_photos]

        likes_and_sizes = list(zip(likes, sizes))
        list_of_lists = [list(elem) for elem in likes_and_sizes]
        albums = dict(zip(urls, list_of_lists))
        json_photos = {}
        photos_name = []

        for url in albums.keys():
            r = requests.get(url, allow_redirects=True)
            if os.path.isfile(f'{albums[url][0]}.jpg') == True:
                open(f'{albums[url][0]}.jpg', 'wb').write(r.content)
                json_photos[f'{albums[url][0]}.jpg'] = f'{albums[url][1]}'
                photos_name.append(f'{albums[url][0]}.jpg')
                print(f'File  {albums[url][0]}.jpg is overwritten ')
            else:
                open(f'{albums[url][0]}.jpg', 'wb').write(r.content)
                json_photos[f'{albums[url][0]}.jpg'] = f'{albums[url][1]}'
                photos_name.append(f'{albums[url][0]}.jpg')
                print(f'{albums[url][0]}.jpg is downloaded successfully')

        json_photos_list = [[k,v] for k,v in json_photos.items()]
        json_file = []
        for i in range(0, len(json_photos_list)):
            json_file.append({"file_name": json_photos_list[i][0], "size": json_photos_list[i][1]})

        with open("photos.json", "w", encoding="cp1251") as f:
            json.dump(json_file, f, ensure_ascii=False, indent=4)

        return photos_name


    def yandex_uploader(self, directory):
        dir_creater = requests.put(f'https://cloud-api.yandex.net:443/v1/disk/resources?path={directory}',
                                   headers={'Authorization': f'OAuth {self.Ya_token}'}, )
        for photo in self.download_photo():
            response = requests.get(f'https://cloud-api.yandex.net:443/v1/disk/resources/upload?path={directory}%2F{photo}',
                                headers={'Authorization': f'OAuth {self.Ya_token}'})
            info = response.json()
            href = info['href']
            with open(f'{photo}', 'rb') as f:
                _file = f.read()
                _ = requests.put(href, data=_file)
            print(f'{photo} is uploaded to Ya_DISK')

        print('All files are successfully downloaded')


vk = ''
id = 000000
ya = '00000000000000'
photo_quantity = 5
director = 'test_file'

if __name__ == '__main__':
    person_1 = Photo_Uploader(vk, id, ya, photo_quantity)
    answer = input('Хотите скачать фото на компьютер нажмите 1, хотите скачать и загрузить на Диск нажмите 2: ')
    if answer == '1':
        person_1.download_photo()
    elif answer == '2':
        person_1.yandex_uploader(director)
    else:
        print("Вы ввели неправильную команду")