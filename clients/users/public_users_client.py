import allure
from httpx import Response
from clients.api_client import ApiClient
from clients.public_http_builder import get_public_http_builder
from clients.users.user_schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.routes import APIRoutes


class PublicUsersClient(ApiClient):
    """
    Клиент для работы с эндпоинтами публичных пользователей.

    Наследуется от базового ApiClient и добавляет специализированные методы
    для взаимодействия с пользователями.
    """

    @allure.step("Create user")
    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """
        Создает нового пользователя через API.

        Отправляет POST-запрос на эндпоинт /api/v1/users с данными пользователя
        в формате JSON.

        Args:
            request (CreateUserSchema): модель с данными нового пользователя.
                Должен содержать поля: email, password, lastName, firstName, middleName.

        Returns:
            Response: Объект ответа от сервера (httpx.Response).
                Содержит статус запроса и тело ответа (например, данные созданного пользователя).
        """

        return self.post(APIRoutes.USERS, json=request.model_dump(by_alias=True))

    def create_user(self, request: CreateUserRequestSchema) -> CreateUserResponseSchema:
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)

def get_public_user_client() -> PublicUsersClient:
    """
    Функция создаёт экземпляр PublicUsersClient с уже настроенным HTTP-клиентом.
    :return: Готовый к использованию PublicUsersClient.
    """
    return PublicUsersClient(client=get_public_http_builder())