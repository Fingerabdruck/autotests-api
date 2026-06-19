import http
import pytest
from authentication.authentication_client import get_authentication_client
from authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_user_client
from clients.users.user_schema import CreateUserRequestSchema
from tools.assertions.authentication import assert_login_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema

@pytest.mark.authentication
@pytest.mark.regression
def test_login() -> None:
    """Выполняет тестовый сценарий успешной авторизации пользователя.
    Последовательность действий:
    1. Инициализируется публичный клиент пользователей.
    2. Генерируется объект запроса на создание пользователя (с фейковыми данными).
    3. Пользователь создаётся через публичный API методом ``create_user_api``.
    4. На основе данных созданного пользователя формируется объект аутентификации.
    5. Инициализируется клиент аутентификации и выполняется запрос ``login_api``.
    6. Ответ валидируется: проверяется статус-код, бизнес‑логика ответа и JSON Schema.
    """
    public_user_client = get_public_user_client()
    create_user_request = CreateUserRequestSchema()
    public_user_client.create_user_api(create_user_request)

    authentication_user = AuthenticationUserSchema(
        email=create_user_request.email,
        password=create_user_request.password,
    )
    authentication_client = get_authentication_client()
    login_response = authentication_client.login_api(authentication_user)
    login_response_data = LoginResponseSchema.model_validate_json(login_response.text)

    assert_status_code(login_response.status_code, http.HTTPStatus.OK), 'Некорректный статус-код ответа'
    assert_login_response(login_response_data), "Некорректный ответ на запрос авторизации пользователя"
    print("Пользователь успешно авторизован!")
    validate_json_schema(login_response.json(), login_response_data.model_json_schema())





