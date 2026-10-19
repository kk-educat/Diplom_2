import allure
import pytest

from helpers import ClientAPI
from helpers import User


class TestCreateUser:
    @allure.title('Тест-кейс создания уникального пользователя')
    def test_create_unique_user(self, data_for_user_deletion):
        payload = User().get_new_user_data()
        # отправляем тестируемый запрос
        response = ClientAPI().create_user(payload)
        # проверка результатов
        assert 200 == response.status_code
        response_data = response.json()
        assert 'accessToken' in response_data
        # сохраняем токен авторизации созданного пользователя для его дальнейшего удаления
        data_for_user_deletion['accessToken'] = response_data['accessToken']
        # продолжаем проверку результатов
        assert 'success' in response_data and True == response_data['success']

    @allure.title('Тест-кейс создания пользователя, который уже зарегистрирован')
    def test_create_not_unique_user(self, user_data):
        payload = {
            "email": user_data["email"],
            "password": user_data["password"],
            "name": user_data["name"]
        }
        # отправляем тестируемый запрос
        response = ClientAPI().create_user(payload)
        # проверка результатов
        assert 403 == response.status_code
        response_data = response.json()
        assert 'success' in response_data and False == response_data['success']
        assert 'message' in response_data and 'User already exists' == response_data['message']

    @allure.title('Тест-кейс создания пользователя без одного из обязательных полей')
    @pytest.mark.parametrize('missed_element', ["email", "password", "name"])
    def test_create_user_without_necessarily_param(self, missed_element):
        payload = User().get_new_user_data()
        # удаляем одно из обязательных полей
        del payload[missed_element]
        # отправляем тестируемый запрос
        response = ClientAPI().create_user(payload)
        # проверка результатов
        assert 403 == response.status_code
        response_data = response.json()
        assert 'success' in response_data and False == response_data['success']
        assert 'message' in response_data and 'Email, password and name are required fields' == response_data['message']
