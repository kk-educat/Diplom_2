import allure
import random
import string

from helpers import ClientAPI


class TestCreateOrder:
    @allure.title('Тест-кейс создания заказа НЕавторизованным пользователем')
    def test_create_order_without_auth(self, ingredients_data):
        # отправляем тестируемый запрос
        response = ClientAPI().create_order(ingredients_data)
        # проверка результатов
        assert 200 == response.status_code
        response_data = response.json()
        assert 'success' in response_data and True == response_data['success']

    @allure.title('Тест-кейс создания заказа авторизованным пользователем с ингредиентами')
    def test_create_order_with_auth(self, ingredients_data, user_data):
        # отправляем тестируемый запрос
        response = ClientAPI().create_order(ingredients_data, user_data["accessToken"])
        # проверка результатов
        assert 200 == response.status_code
        response_data = response.json()
        assert 'success' in response_data and True == response_data['success']

    @allure.title('Тест-кейс создания заказа без ингредиентов')
    def test_create_order_without_ingredients(self, user_data):
        data = {'ingredients': []}
        # отправляем тестируемый запрос
        response = ClientAPI().create_order(data, user_data["accessToken"])
        # проверка результатов
        assert 400 == response.status_code
        response_data = response.json()
        assert 'success' in response_data and False == response_data['success']
        assert 'message' in response_data and 'Ingredient ids must be provided' == response_data['message']

    @allure.title('Тест-кейс создания заказа с неверным хешем одного из ингредиентов')
    def test_create_order_ingredient_incorrect_hash(self, ingredients_data, user_data):
        # сохраняем полученный от фикстуры корректный хеш ингредиента в переменную 
        ingr = ingredients_data["ingredients"][1]
        # генерируем строку из 5 случайных букв
        random_chars = ''.join(random.choices(string.ascii_letters, k=5))
        # в хеше ингредиента заменяем 5 символов с 10 до 15 подготовленной строкой из 5 случайных букв
        ingredients_data["ingredients"][1] = ingr[:10] + random_chars + ingr[15:]
        # отправляем тестируемый запрос
        response = ClientAPI().create_order(ingredients_data, user_data["accessToken"])
        # проверка результатов
        assert 500 == response.status_code
