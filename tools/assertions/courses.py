from clients.courses.courses_schema import UpdateCoursesRequestSchema, UpdateCoursesResponseSchema, CourseSchema, \
    GetCoursesResponseSchema, CreateCoursesResponseSchema, CreateCoursesRequestSchema
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.files import assert_file
from tools.assertions.users import assert_user


def assert_update_course_response(
        request: UpdateCoursesRequestSchema,
        response: UpdateCoursesResponseSchema
):
    """
    Проверяет, что ответ на обновление курса содержит те же данные, что были переданы в запросе.
    :param request: Модель запроса (UpdateCoursesRequestSchema), содержащая отправленные для обновления данные.
    :param response: Ответ от API (UpdateCoursesResponseSchema) с фактическими данными обновленного курса.
    :raises AssertionError: Если значения полей в ответе сервера не совпадают с переданными в запросе.
    """
    assert_equal(response.course.title, request.title, "title")
    assert_equal(response.course.max_score, request.max_score, "max_score")
    assert_equal(response.course.min_score, request.min_score, "min_score")
    assert_equal(response.course.description, request.description, "description")
    assert_equal(response.course.estimated_time, request.estimated_time, "estimated_time")


def assert_course(actual: CourseSchema, expected: CourseSchema):
    """
    Проверяет, что фактические данные курса соответствуют ожидаемым.
    :param actual: Фактические данные курса.
    :param expected: Ожидаемые данные курса.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")

    assert_file(actual.preview_file, expected.preview_file)
    assert_user(actual.created_by_user_id, expected.created_by_user_id)

def assert_get_courses_response(
        get_courses_response: GetCoursesResponseSchema,
        create_course_responses: list[CreateCoursesResponseSchema],
):
    """
    Проверяет, что ответ на получение списка курсов соответствует ответам на их создание.
    :param get_courses_response: Ответ API при запросе списка курсов.
    :param create_course_responses: Список API ответов при создании курсов.
    :raises AssertionError: Если данные курсов не совпадают.
    """
    assert_length(get_courses_response.courses, create_course_responses, "courses")

    for index, create_course_response in enumerate(create_course_responses):
        assert_course(get_courses_response.courses[index], create_course_response.course)


def assert_create_course_response(request: CreateCoursesRequestSchema, response: CreateCoursesResponseSchema):
    """
    Проверяет, что фактические данные созданного курса соответствуют ожидаемым данным из запроса.

    :param request: Ожидаемые данные (модель CreateCoursesRequestSchema), отправленные при создании.
    :param response: Фактический ответ от API (модель CreateCoursesResponseSchema).
    :raises AssertionError: Если значения полей фактического курса не совпадают с ожидаемыми.
    """
    assert_equal(response.course.title, request.title, "title")
    assert_equal(response.course.max_score, request.max_score, "max_score")
    assert_equal(response.course.min_score, request.min_score, "min_score")
    assert_equal(response.course.description, request.description, "description")
    assert_equal(response.course.estimated_time, request.estimated_time, "estimated_time")

    assert_equal(response.course.preview_file.id, request.preview_file_id, "file_id")
    assert_equal(response.course.created_by_user_id.id, request.created_by_user_id, "created_by_user_id")