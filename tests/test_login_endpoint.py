import allure
import pytest

from helpers import ClientAPI


class TestLogin:
    @allure.title('Тест-кейс логина под существующим пользователем')
    def test_existing_user_login(self, user_data):
        # сохраняем для дальнейшей проверки
        user_name = user_data["name"]
        # удаляем из данных пользователя поля, не используемые во время логина
        del user_data["name"], user_data["accessToken"]
        # отправляем тестируемый запрос
        response = ClientAPI().login(user_data)
        # проверка результатов
        assert 200 == response.status_code
        response_data = response.json()
        assert 'success' in response_data and True == response_data['success']
        assert 'accessToken' in response_data
        assert 'refreshToken' in response_data
        assert 'user' in response_data
        assert user_data['email'] == response_data['user']['email'] and user_name == response_data['user']['name']

    @allure.title('Тест-кейс логина с неверным логином/паролем')
    @pytest.mark.parametrize('wrong_element', ["email", "password"])
    def test_login_with_wrong_necessarily_field(self, wrong_element, user_data):
        # удаляем из данных пользователя поля, не используемые во время логина
        del user_data["name"], user_data["accessToken"]
        # модифицируем поле, которое должно быть неверным
        user_data[wrong_element] = 'DEAD' + user_data[wrong_element]
        # отправляем тестируемый запрос
        response = ClientAPI().login(user_data)
        # проверка результатов
        assert 401 == response.status_code
        response_data = response.json()
        assert 'success' in response_data and False == response_data['success']
        assert 'message' in response_data and 'email ог password аге incorrect' == response_data['message']
