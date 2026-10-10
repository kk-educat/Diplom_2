import requests
from faker import Faker

import data as d


class ClientAPI:

    def get_ingredients(self):
        return requests.get(d.GET_INGREDIENTS_ENDPOINT)

    def create_order(self, data, token=None):
        if token:
            return requests.post(d.CREATE_ORDER_ENDPOINT, json = data, headers={'Authorization': token})
        else:
            return requests.post(d.CREATE_ORDER_ENDPOINT, json = data)

    def create_user(self, data):
        return requests.post(d.CREATE_USER_ENDPOINT, json = data)

    def delete_user(self, token):
        return requests.delete(d.DELETE_USER_ENDPOINT, headers={"Authorization": token})

    def login(self, data):
        return requests.post(d.LOGIN_ENDPOINT, json = data)


class User:
    def get_new_user_data(self):
        fake = Faker('ru_RU')
        data = {
            "email": fake.email(),
            "password": fake.password(),
            "name": fake.first_name()
        }
        return data
