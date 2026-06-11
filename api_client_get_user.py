from clients.private_http_builder import AuthenticationUserDict
from clients.users.private_users_client import get_private_users_client
from clients.users.public_users_client import get_public_user_client, CreateUserRequestDict
from tools.fakers import get_random_email

""" 
Инициализация публичного клиента для регистрации нового пользователя без авторизации
"""
public_user_client = get_public_user_client()

"""
Формирование данных запроса на создание пользователя с рандомным email и фиксированным паролем
"""
create_user_request = CreateUserRequestDict(
    email = get_random_email(),
    password = "string",
    lastName = "string",
    firstName = "string",
    middleName = "string",
)

"""
Отправка запроса на регистрацию пользователя и получение ответа от сервера
"""
create_user_response = public_user_client.create_user(create_user_request)
print("Create user data: ", create_user_response)

"""
Подготовка данных для авторизации (email и пароль только что созданного пользователя)
"""
authentication_user = AuthenticationUserDict(
    email = create_user_request['email'],
    password = create_user_request['password'],
)
"""
Создание приватного клиента
"""
private_user_client = get_private_users_client(authentication_user)
get_user_response = private_user_client.get_user(create_user_response['user']['id'])
print("Get user data: ", get_user_response)