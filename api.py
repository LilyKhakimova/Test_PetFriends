import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email, password):
        '''Метод делает get запрос к API  сервера и возвращает статус запроса и резуьлтат в формате
        JSON с уникальным ключем пользователя. найденного по указанным email и паролю'''
        headers = {
            "email": email,
            "password": password
        }
        res = requests.get(self.base_url+"api/key", headers=headers)
        status = res.status_code

        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        '''Метод деалет get запрос к API сервера и возвращает: статус запроса и результат в формате JSON
        со списком найденных питомцев, совпадающих с фильтром'''
        headers = {"auth_key": auth_key["key"]}
        filter = {"filter": filter}

        res = requests.get(self.base_url+"api/pets", headers=headers, params=filter)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key, name, animal_type, age, pet_photo):
        '''Метод делает post запрос к API сервера, добавляет данные data на сайт PetFriends и
        возвращает код статуса запроса и результат в формате JSPN с информацией о животном'''
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key, pet_id, name,
                        animal_type, age) :
        """Метод делает put запрос к API сервера о обновлении данных питомуа по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet_without_photo(self, auth_key, name, animal_type, age):
        '''Метод делает post запрос к API сервера, добавляет новые данные из data на сайт
        и возвращает код статуса запроса и результат в формате json с информацией о животном.'''
        headers = {
            'auth_key': auth_key['key'],
        }
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def test_add_pet_photo(self, auth_key, pet_id, pet_photo) :
        """Метод делает post запрос к API сервера и добавляет фото питомца, а также возвращает статус
        запроса и результат в формате JSON с данными добавленного питомца"""
        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'images/jpg')
                    })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def delete_pet(self, auth_key, pet_id) :
        """Метод делает delete запрос к API сервера на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении"""
        headers = {'auth_key': auth_key['key'], 'pet_id': pet_id}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def create_pet_simple(self, auth_key, name, animal_type, age):
        """Метод делает post к API сервера о добавлении данных о новом питомце без фото и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца без фото"""
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }
        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_photo_pet(self, auth_key, pet_id, pet_photo) :
        """Метод делает post к API сервера, добавляет фото питомца и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""
        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'images/jpg')
                    })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
