from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from tools.assertions.base import assert_equal


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
