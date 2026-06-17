from pydantic import BaseModel, EmailStr, Field, ValidationError
from clients.users.public_users_client import CreateUserRequestDict
from tools.fakers import Fake


class UserSchema(BaseModel):
    id: str
    email: EmailStr
    last_name: str = Field(alias='lastName')
    first_name: str = Field(alias='firstName')
    middle_name: str = Field(alias='middleName')


class CreateUserRequestSchema(BaseModel):
    email: EmailStr = Field(default="test_email@testing_api.ru")
    password: str
    last_name: str = Field(alias='lastName')
    first_name: str = Field(alias='firstName')
    middle_name: str = Field(alias='middleName')


class CreateUserResponseSchema(BaseModel):
    user: UserSchema


# 1. Прямое создание (используем алиасы, как требует Pydantic по умолчанию)
create_user_schema = CreateUserRequestSchema(
    email=get_random_email(),
    password="Password",
    lastName="Ivanov",
    firstName="Ivan",
    middleName="Ivanovich",
)

print("Create user schema: ", create_user_schema)


# 2. Создание из словаря (ключи словаря соответствуют алиасам)
create_user_dict = {
    "email": get_random_email(),
    "password": "Password",
    "lastName": "Ivanov",
    "firstName": "Ivan",
    "middleName": "Ivanovich"
}

create_user_model = CreateUserRequestSchema(**create_user_dict)
print("Create user model: ", create_user_model)
print("Dump (snake_case): ", create_user_model.model_dump())
print("Dump (camelCase): ", create_user_model.model_dump(by_alias=True))


# 3. Создание из JSON (email подтянется из default)
create_user_json = """
{
    "password": "Password",
    "lastName": "Ivanov",
    "firstName": "Ivan",
    "middleName": "Ivanovich"
}
"""

create_user_json_model = CreateUserRequestSchema.model_validate_json(create_user_json)
print("Create user json model: ", create_user_json_model)


# 4. Проверка ошибок валидации
try:
    user = CreateUserRequestSchema(
        email=".ru",            # Специально передаем невалидный email
        password="Password",
        lastName="Ivanov",
        firstName="Ivan",
        middleName="Ivanovich",
    )
except ValidationError as error:
    print("\nОжидаемая ошибка валидации:")
    print(error)