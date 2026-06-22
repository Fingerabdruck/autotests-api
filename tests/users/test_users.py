import http
import pytest
from clients.users.public_users_client import get_public_user_client, PublicUsersClient
from clients.users.user_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_get_user_response
from tools.fakers import fake



@pytest.mark.users
@pytest.mark.regression
class TestUsers:
    @pytest.mark.parametrize("email", ["mail.ru", "gmail.com", "example.com"])
    def test_create_users(self, email: str, public_user_client: PublicUsersClient):

        generated_email = fake.email(domain=email)
        request = CreateUserRequestSchema(email=generated_email)
        response = public_user_client.create_user_api(request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)
        assert_status_code(response.status_code, http.HTTPStatus.OK)
        assert_create_user_response(request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())


    def test_get_user_me(self, private_users_client, function_user):

        response = private_users_client.get_user_me_api()
        response_data = GetUserResponseSchema.model_validate_json(response.text)
        assert_status_code(response.status_code, http.HTTPStatus.OK)
        assert_get_user_response(response_data, function_user.response)
        validate_json_schema(response.json(), response_data.model_json_schema())