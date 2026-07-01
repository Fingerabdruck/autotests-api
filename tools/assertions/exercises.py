import allure

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    ExerciseSchema, GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema, \
    GetExercisesResponseSchema
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.errors import assert_internal_error_response

@allure.step("Check exercise")
def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Проверяет, что фактические данные упражнения соответствуют ожидаемым.

    :param actual: Фактические данные упражнения (модель ExerciseSchema), полученные от API.
    :param expected: Ожидаемые данные упражнения (модель ExerciseSchema) для сравнения.
    :raises AssertionError: Если значения полей фактического упражнения не совпадают с ожидаемыми.
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.course_id, expected.course_id, "course_id")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.order_index, expected.order_index, "order_index")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")


@allure.step("Check exercise response")
def assert_create_exercise_response(request: CreateExerciseRequestSchema, response: CreateExerciseResponseSchema):
    """
    Проверяет, что фактические данные созданного упражнения соответствуют ожидаемым данным из запроса.

    :param request: Ожидаемые данные (модель CreateExerciseRequestSchema), отправленные при создании упражнения.
    :param response: Фактический ответ от API (модель CreateExerciseResponseSchema), содержащий созданное упражнение.
    :raises AssertionError: Если значения полей фактического упражнения не совпадают с ожидаемыми.
    """
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.course_id, request.course_id, "course_id")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")

@allure.step("Check get exercise response")
def assert_get_exercise_response(
        actual_response: GetExerciseResponseSchema,
        expected_response: CreateExerciseResponseSchema
):
    """
    Проверяет, что ответ на получение задания соответствует данным, полученным при его создании.

    :param actual_response: Фактический ответ API при получении задания (GET-запрос).
    :param expected_response: Ожидаемый ответ API, сохраненный при создании задания (POST-запрос из фикстуры).
    :raises AssertionError: Если данные задания не совпадают.
    """
    assert_exercise(actual_response.exercise, expected_response.exercise)

@allure.step("Check get exercises response")
def assert_get_exercises_response(
        get_exercises_response: GetExercisesResponseSchema,
        create_exercise_responses: list[CreateExerciseResponseSchema],
):
    """
    Проверяет, что ответ на получение списка заданий соответствует ответам на их создание.

    :param get_exercises_response: Ответ API при запросе списка заданий (GetExercisesResponseSchema).
    :param create_exercise_responses: Список эталонных ответов API, сохраненных при создании заданий (CreateExerciseResponseSchema).
    :raises AssertionError: Если количество заданий или их данные не совпадают.
    """
    assert_length(get_exercises_response.exercises, create_exercise_responses, "exercises")

    for index, create_exercise_response in enumerate(create_exercise_responses):
        assert_exercise(get_exercises_response.exercises[index], create_exercise_response.exercise)

@allure.step("Check update exercise response")
def assert_update_exercise_response(request: UpdateExerciseRequestSchema, response: UpdateExerciseResponseSchema):
    """
    Проверяет, что фактические данные обновленного упражнения соответствуют отправленным в запросе.

    :param request: Модель запроса (UpdateExerciseRequestSchema), содержащая отправленные для обновления данные.
    :param response: Ответ от API (UpdateExerciseResponseSchema) с фактическими данными обновленного упражнения.
    :raises AssertionError: Если значения полей в ответе сервера не совпадают с переданными в запросе.
    """
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")

@allure.step("Check exercise not found response")
def assert_exercise_not_found_response(response: InternalErrorResponseSchema):
    """
    Проверяет, что тело ответа содержит ошибку о том, что задание не найдено.

    :param response: Фактический ответ от API с ошибкой (модель InternalErrorResponseSchema).
    """
    expected_error = InternalErrorResponseSchema(details="Exercise not found")
    assert_internal_error_response(actual=response, expected=expected_error)