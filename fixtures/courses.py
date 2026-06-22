from pydantic import BaseModel
import pytest

from clients.courses.courses_client import get_private_course_client, CoursesClient
from clients.courses.courses_schema import CreateCoursesRequestSchema, CreateCoursesResponseSchema
from fixtures.files import FileFixture
from fixtures.user import UserFixture
from testdata.files.files_client import FilesClient

class CourseFixture(BaseModel):
    request: CreateCoursesRequestSchema
    response: CreateCoursesResponseSchema

@pytest.fixture
def courses_client(function_user: UserFixture) -> CoursesClient:
    return get_private_course_client(function_user.authentication_user)

@pytest.fixture
def function_course(
        courses_client: CoursesClient,
        function_user: UserFixture,
        function_file: FileFixture
) -> CourseFixture:
    request = CreateCoursesRequestSchema(
        preview_file_id=function_file.response.file.id,
        created_by_user_id=function_user.response.user.id)
    response = courses_client.create_course(request)
    return CourseFixture(request=request, response=response)
