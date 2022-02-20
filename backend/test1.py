import requests

AUTH_TOKEN = 'b77dee7c2aa4307af442d40fec0df5b63ad73876'


def create_user():
    url = 'http://localhost:8000/api/users/'
    data = {
        'email': 'vpupkin@yandex.ru',
        'username': 'vp',
        'first_name': 'Вася',
        'last_name': 'Пупкин',
        'password': 'California05131',
    }
    request = requests.post(url, data)
    print(request.json())


def get_auth_token():
    url = 'http://localhost:8000/api/auth/token/login/'
    data = {
        'email': 'vpupkin@yandex.ru',
        'password': 'California123321',
    }
    request = requests.post(url, data)
    print(request.json())


def get_users_list():
    url = 'http://localhost:8000/api/users/'
    headers = {'Authorization': f'Token {AUTH_TOKEN}'}
    request = requests.get(url, headers=headers)
    print(request.json())


def get_user_profile():
    url = 'http://localhost:8000/api/users/2/'
    headers = {'Authorization': f'Token {AUTH_TOKEN}'}
    request = requests.get(url, headers=headers)
    print(request.json())


def get_me():
    url = 'http://localhost:8000/api/users/me/'
    headers = {'Authorization': f'Token {AUTH_TOKEN}'}
    request = requests.get(url, headers=headers)
    print(request.json())


def set_password():
    url = 'http://localhost:8000/api/users/set_password/'
    headers = {'Authorization': f'Token {AUTH_TOKEN}'}
    data = {
        "new_password": "California05131",
        "current_password": "California123321"
    }
    request = requests.post(url, data=data, headers=headers)
    print(request.json())


def logout():
    url = 'http://localhost:8000/api/auth/token/logout/'
    headers = {'Authorization': f'Token {AUTH_TOKEN}'}
    request = requests.post(url, headers=headers)
    print(request)


if __name__ == '__main__':
    logout()
