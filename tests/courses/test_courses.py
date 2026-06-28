from http import HTTPStatus

import pytest

from clients.courses.courses_client import CoursesClient
from clients.courses.courses_schema import UpdateCoursesRequestSchema, UpdateCoursesResponseSchema, \
    GetCoursesQuerySchema, GetCoursesResponseSchema, CreateCoursesRequestSchema, CreateCoursesResponseSchema
from fixtures.courses import CourseFixture
from fixtures.files import FileFixture
from fixtures.user import UserFixture
from tools.assertions.base import assert_status_code
from tools.assertions.courses import assert_update_course_response, assert_get_courses_response, \
    assert_create_course_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.courses
@pytest.mark.regression
class TestCourses:
    def test_get_course(self, courses_client: CoursesClient, function_course: CourseFixture, function_user: UserFixture):
        query = GetCoursesQuerySchema(user_id=function_user.response.user.id)
        response = courses_client.get_courses_api(query)
        assert_status_code(response.status_code, HTTPStatus.OK)
        response_data = GetCoursesResponseSchema.model_validate_json(response.text)

        assert_get_courses_response(response_data, [function_course.response])
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_course(self, courses_client: CoursesClient, function_course: CourseFixture):
        request = UpdateCoursesRequestSchema()
        response = courses_client.update_course_api(function_course.response.course.id, request)
        assert_status_code(response.status_code, HTTPStatus.OK)
        response_data = UpdateCoursesResponseSchema.model_validate_json(response.text)

        assert_update_course_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_create_course(self, courses_client: CoursesClient, function_user: UserFixture, function_file: FileFixture):
        request = CreateCoursesRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id)
        response = courses_client.create_course_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)
        response_data = CreateCoursesResponseSchema.model_validate_json(response.text)
        assert_create_course_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())
