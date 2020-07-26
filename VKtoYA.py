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
    def __init__(self, VK_token, id_number, Ya_token):
       self.VK_token = VK_token
       self.id_number = id_number,
       self.Ya_token = Ya_token

    def get_photo(self):
        response = requests.get(
            'https://api.vk.com/method/photos.get',
            params={
                'owner_id': self.id_number,
                'album_id': 'profile',
                'access_token': self.VK_token,
                'v': '5.120',
                'extended': 1,
            }
        )
        return response.json()


    def download_photo(self, number_of_photos):
        photos = answer['response']['items']
        last_photos = photos[-(number_of_photos):]
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
            if os.path.isfile(f'{albums[url]}.jpg') == True:
                open(f'{albums[url][0]}_1.jpg', 'wb').write(r.content)
                json_photos[f'{albums[url][0]}_1.jpg']= f'{albums[url][1]}'
                photos_name.append(f'{albums[url][0]}_1.jpg')
                print(f'{albums[url][0]}_1.jpg is downloaded successfully')
            else:
                open(f'{albums[url][0]}.jpg', 'wb').write(r.content)
                json_photos[f'{albums[url][0]}.jpg']= f'{albums[url][1]}'
                photos_name.append(f'{albums[url][0]}.jpg')
                print(f'{albums[url][0]}.jpg is downloaded successfully')

        json_photos_list = [[k,v] for k,v in json_photos.items()]
        # print(json_photos_list)
        json_file = []
        for i in range(0, len(json_photos_list)):
            json_file.append({"file_name": json_photos_list[i][0], "size": json_photos_list[i][1]})

        with open("photos.json", "w", encoding="cp1251") as f:
            json.dump(json_file, f, ensure_ascii=False, indent=4)

        return photos_name


    def yandex_uploader(self, directory):
        dir_creater = requests.put(f'https://cloud-api.yandex.net:443/v1/disk/resources?path={directory}',
                                headers={'Authorization': f'OAuth {self.Ya_token}'}, )

        for photo in photo_list:
            response = requests.get(f'https://cloud-api.yandex.net:443/v1/disk/resources/upload?path={directory}%2F{photo}',
                                headers={'Authorization': 'OAuth AgAAAAAcud6tAADLWzyhY5ZgpkX7lSqDp8GbPSE'})
            info = response.json()
            href = info['href']
            with open(f'{photo}', 'rb') as f:
                _file = f.read()
                r = requests.put(href, data=_file)
                print(f'{photo} is uploaded to Ya_DISK')

        print('All files are successfully downloaded')

vk_token = input('Пожалуйста введите свой ВК-токен: ')
id_user = input('Пожалуйста введите id нужного вам юзера: ')
ya_token = input('Пожалуйста введите свой токен от Полигона: ')
ya_directory = input('Пожалуйста введите навание папки на Яндекс Диске: ')

with open('username_info.txt', 'w') as f:
    f.write(f'vk_token: {vk_token}\n')
    f.write(f'id_user: {id_user}\n')
    f.write(f'ya_token: {ya_token}\n')

person_1 = Photo_Uploader(vk_token, id_user, ya_token)
answer = person_1.get_photo()
photo_list = person_1.download_photo(4)
person_1.yandex_uploader(ya_directory)