from typing_extensions import TypedDict
from httpx import Response, Client
from clients.api_client import ApiClient
from clients.public_http_builder import get_public_http_builder

class User(TypedDict):
    """
    Описание структуры пользователя.
    """
    id: str
    email: str
    lastName: str
    firstName: str
    middleName: str

class CreateUserRequestDict(TypedDict):
    """
    Описание структуры запроса на создание пользователя.
    """
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str

class CreateUserResponse(TypedDict):
    """
    Описание структуры ответа создания пользователя.
    """
    user: User

class PublicUsersClient(ApiClient):
    """
    Клиент для работы с эндпоинтами публичных пользователей.

    Наследуется от базового ApiClient и добавляет специализированные методы
    для взаимодействия с пользователями.
    """

    def create_user_api(self, request: CreateUserRequestDict) -> Response:
        """
        Создает нового пользователя через API.

        Отправляет POST-запрос на эндпоинт /api/v1/users с данными пользователя
        в формате JSON.

        Args:
            request (CreateUserDict): Словарь с данными нового пользователя.
                Должен содержать поля: email, password, lastName, firstName, middleName.

        Returns:
            Response: Объект ответа от сервера (httpx.Response).
                Содержит статус запроса и тело ответа (например, данные созданного пользователя).

        Example:
            >>> user_data = {
            ...     "email": "test@example.com",
            ...     "password": "securepass",
            ...     "lastName": "Ivanov",
            ...     "firstName": "Ivan",
            ...     "middleName": "Ivanovich"
            ... }
            >>> response = client.create_user_api(user_data)
            >>> print(response.status_code)
            201
        """
        return self.post('/api/v1/users', json=request)

    def create_user(self, request: CreateUserRequestDict) -> CreateUserResponse:
        response = self.create_user_api(request)
        return response.json()

def get_public_user_client() -> PublicUsersClient:
    """
    Функция создаёт экземпляр PublicUsersClient с уже настроенным HTTP-клиентом.
    :return: Готовый к использованию PublicUsersClient.
    """
    return PublicUsersClient(client=get_public_http_builder())