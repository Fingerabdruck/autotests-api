from http import HTTPStatus
import pytest
from authentication.authentication_client import AuthenticationClient
from authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from fixtures.user import UserFixture
from tools.assertions.authentication import assert_login_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema

@pytest.mark.authentication
@pytest.mark.regression
def test_login(function_user: UserFixture, authentication_client: AuthenticationClient):
    """Выполняет тестовый сценарий успешной авторизации пользователя.
    Последовательность действий:
    1. Инициализируется публичный клиент пользователей.
    2. Генерируется объект запроса на создание пользователя (с фейковыми данными).
    3. Пользователь создаётся через публичный API методом ``create_user_api``.
    4. На основе данных созданного пользователя формируется объект аутентификации.
    5. Инициализируется клиент аутентификации и выполняется запрос ``login_api``.
    6. Ответ валидируется: проверяется статус-код, бизнес‑логика ответа и JSON Schema.
    """

    request = LoginRequestSchema(email=function_user.email,password=function_user.password,)
    response = authentication_client.login_api(request)
    response_data = LoginResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK), 'Некорректный статус-код ответа'
    assert_login_response(response_data), "Некорректный ответ на запрос авторизации пользователя"
    print("Пользователь успешно авторизован!")
    validate_json_schema(response.json(), response_data.model_json_schema())





