import pytest
from helpers import User
from helpers import ClientAPI


@pytest.fixture
def user_data():
    payload = User().get_new_user_data()
    response = ClientAPI().create_user(payload)
    data = {
        "email": payload["email"],
        "password": payload["password"],
        "name": payload["name"],
        "accessToken": response.json()["accessToken"]
    }
    yield data
    ClientAPI().delete_user(data["accessToken"])

@pytest.fixture
def data_for_user_deletion():
    # возвращаем в тест-кейс словарь, в который тест-кейс сохранит track созданного заказа
    data = {'accessToken': 0}
    yield data
    # когда тест-кейс отработает, удаляем созданный в нем заказ, если значение track было сохранено
    if data['accessToken'] != 0:
        ClientAPI().delete_user(data['accessToken'])

@pytest.fixture
def ingredients_data():
    response = ClientAPI().get_ingredients()
    response_data = response.json()
    ingredient_0 = response_data['data'][0]['_id']
    ingredient_1 = response_data['data'][1]['_id']
    data = {'ingredients': [ingredient_0, ingredient_1]}
    return data
