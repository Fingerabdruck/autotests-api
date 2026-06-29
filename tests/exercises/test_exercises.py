from http import HTTPStatus

import pytest

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, \
    assert_update_exercise_response, assert_exercise_not_found_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
    def test_create_exercise(self, exercises_client: ExercisesClient, function_course: CourseFixture):
        request = CreateExerciseRequestSchema()
        response = exercises_client.create_exercise_api(request)
        assert_status_code(response.status_code, HTTPStatus.OK)
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)
        assert_create_exercise_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_exercise(self, exercises_client: ExercisesClient, function_course: CourseFixture, function_exercise: ExerciseFixture):
        response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        assert_status_code(response.status_code, HTTPStatus.OK)
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)
        assert_get_exercise_response(response_data, function_exercise.response)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_exercise(self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture):
        request = UpdateExerciseRequestSchema()
        response = exercises_client.update_exercise_api(function_exercise.response.exercise.id, request)
        assert_status_code(response.status_code, HTTPStatus.OK)
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)
        assert_update_exercise_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())


    def test_delete_exercise(self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture):
        delete_response = exercises_client.delete_exercise_api(function_exercise.response.exercise.id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_delete_response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        assert_status_code(get_delete_response.status_code, HTTPStatus.NOT_FOUND)
        get_delete_response_data = InternalErrorResponseSchema.model_validate_json(get_delete_response.text)
        assert_exercise_not_found_response(get_delete_response_data)

        validate_json_schema(get_delete_response.json(), get_delete_response_data.model_json_schema())