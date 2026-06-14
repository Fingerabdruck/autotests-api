"""
{
  "course": {
    "id": "string",
    "title": "string",
    "maxScore": 0,
    "minScore": 0,
    "description": "string",
    "previewFile": {
      "id": "string",
      "filename": "string",
      "directory": "string",
      "url": "https://example.com/"
    },
    "estimatedTime": "string",
    "createdByUser": {
      "id": "string",
      "email": "user@example.com",
      "lastName": "string",
      "firstName": "string",
      "middleName": "string"
    }
  }
}
"""

from pydantic import BaseModel, Field, EmailStr, HttpUrl, ValidationError
from sqlalchemy import alias


class UserSchema(BaseModel):
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")

    def get_username(self) -> str:
        return f"{self.first_name} {self.last_name}"

class FileSchema(BaseModel):
    id: str
    filename: str
    directory: str
    url: HttpUrl

class CourseSchema(BaseModel):
    id: str
    title: str
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    description: str
    # Вложенный объект для файла-превью
    preview_file: FileSchema = Field(alias="previewFile")
    # Вложенный объект для пользователя, создавшего курс
    created_by_user: UserSchema = Field(alias="createdByUser")
    estimated_time: str = Field(alias="estimatedTime")

# Инициализируем модель CourseSchema через передачу аргументов
course_default_schema = CourseSchema(
    id="course_id",
    title="python_course",
    maxScore=100,
    minScore=10,
    description="Bla-bla-bla",
    estimatedTime="1 week",
    # Добавили инициализацию вложенной модели FileSchema
    previewFile=FileSchema(
    id="preview_file_id",
    filename="preview_file",
    directory="/users",
    url="http://127.0.0.1:8000/",
    # Добавили инициализацию вложенной модели UserSchema
    createdByUser=UserSchema(
        id="created_by_user_id",
        email="rodip@example.com",
        lastName="Bobrov",
        firstName="Eliza",
        middleName="Yovovich"
    )
)
)

print(course_default_schema)

course_dict = {
    "id": "course_id",
    "title": "python_course",
    "maxScore": 100,
    "minScore": 10,
    "description": "Bla-bla-bla",
    "estimatedTime": "1 week",
    "previewFile": {
        "id": "preview_file_id",
        "url": "http://127.0.0.1:8000/",
        "filename": "preview_file",
        "directory": "/users"
    },
    "createdByUser": {
        "id": "user-id",
        "email": "user@gmail.com",
        "lastName": "Bond",
        "firstName": "Zara",
        "middleName": "Alise"
    }
  }


course_dict_model = CourseSchema(**course_dict)
print("Course dict:", course_dict_model)
print(course_dict_model.model_dump())
print(course_dict_model.model_dump(by_alias=True))

course_json = """
{
    "id": "course_id",
    "title": "python_course",
    "maxScore": 100,
    "minScore": 10,
    "description": "Bla-bla-bla",
    "estimatedTime": "1 week",
    "previewFile": {
        "id": "preview_file_id",
        "url": "http://127.0.0.1:8000/",
        "filename": "preview_file",
        "directory": "/users"
    },
    "createdByUser": {
        "id": "user-id",
        "email": "user@gmail.com",
        "lastName": "Bond",
        "firstName": "Zara",
        "middleName": "Alise"
    }
  }
"""

course_json_model = CourseSchema.model_validate_json(course_json)
print("Course json: ", course_json_model)

# Инициализируем FileSchema c некорректным url
try:
    file = FileSchema(
        id="file-id",
        url="localhost",
        filename="file.png",
        directory="courses",
    )
except ValidationError as error:
    print(error)
    print(error.errors())