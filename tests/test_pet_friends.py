from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    '''Проверяем что код статуса запроса 200 и в переменной result содержится слово key'''
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result


def test_get_all_pets_with_valid_key(filter=""):
    '''Проверяем что код статуса запроса 200 и список всех питомцев не пустой
    Для этого при помощи метода get_app_key() получаем ключ, сохраняем его в переменной
    api_key, затем применяем метод get_list_of_pets() и проверяем статус ответа и то
    что список питомцев не пустой'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0

def test_add_new_pet(name="Песель", animal_type="Собака", age="5", pet_photo="images/Pesel.jpg"):
    '''Проверяем что код статуса запроса 200 и что список с добавленными данными не пустой для этого
        в переменную pet_photo сохраняем путь к файлу фотографии питомца, сохраняем ключ в переменную api_key,
        проверяем статус ответа и что в ответе содержатся добавленные данные.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_update_pet_info(name='Барбос', animal_type='Пес', age='2'):
    '''Проверяем возможность изменения данных питомца'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцы отсутствуют")

def test_add_pet_without_photo(name='Котофей', animal_type='Кот', age='1'):
    '''Проверяем возможность добавления нового питомца без фото'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_add_pet_photo(pet_photo='images/Kote.jpg'):
    '''Проверяем возможность добавления новой фотографии питомца'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.test_add_pet_photo(api_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("Питомцы отсутствуют")


def test_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Карамба", "попугай", "10", "images/Pirat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

def test_get_api_key_with_invalid_password(email=valid_email, password=invalid_password):
    '''Негативное тестирование при вводе неправильного пароля. Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    '''Негативное тестирование при вводе направильного e-mail. Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_add_pet_negative_age_number(name='Карамба', animal_type='Попугай', age='-4', pet_photo='images/Pirat.jpg'):
    '''Негативное тестирование. Добавление питомца с отрицательным числом в переменной age'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert age not in result['age'], 'Ошибка. Введено отрицательное число в поле возраст'

def test_add_pet_with_three_digit_age_number(name='Карамба', animal_type='Попугай', age='123', pet_photo='images/Pirat.jpg'):
    '''Негативное тестирование. Добавление питомца с трехзначным числом в поле age'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    number = result['age']

    assert len(number) < 3, 'Ошибка. Возраст питомца более 100 лет'

def test_add_pet_with_empty_name(name='', animal_type='Суслик', age='7', pet_photo='images/Homa.jpg'):
    '''Негативное тестирование. Добавление питомца с пустым именем'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] != '', 'Ошибка. Не введено имя питомца'

def test_add_pet_with_special_characters_in_type(name='Хома', animal_type='#$%^&*{}|?/><=+_~@', age='20', pet_photo='images/Homa.jpg'):
    '''Негативное тестирование. Добавление питомца с пустым полем в графе "Порода"'''
    symbols = '#$%^&*{}|?/><=+_~@'
    symbol = []
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    for i in symbols:
        if i in result['animal_type']:
            symbol.append(i)
    assert symbol[0] not in result['animal_type'], 'Ошибка. Использованы недопустимые символы в поле "Порода"'
