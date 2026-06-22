from httpx import Client
from authentication.authentication_client import get_authentication_client
from authentication.authentication_schema import LoginRequestSchema
from pydantic import BaseModel
from functools import lru_cache

class AuthenticationUserSchema(BaseModel, frozen=True):
    email: str
    password: str

@lru_cache(maxsize=None)
def get_private_http_builder(user: AuthenticationUserSchema, ) -> Client:
    """
    Функция создаёт экземпляр httpx.Client с аутентификацией пользователя.
    :param user: Объект AuthenticationUserSchema с email и паролем пользователя.
    :return: Готовый к использованию объект httpx.Client с установленным заголовком Authorization.
    """

    authentication_client = get_authentication_client()
    login_request = LoginRequestSchema(email=user.email, password=user.password)
    login_response = authentication_client.login(login_request)
    return Client(timeout=100, base_url='http://localhost:8000', headers={"Authorization": f"Bearer {login_response.token.access_token}"})
