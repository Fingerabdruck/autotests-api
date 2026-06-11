from clients.api_client import ApiClient
from httpx import Response
from typing import TypedDict

from clients.private_http_builder import get_private_http_builder, AuthenticationUserDict
from clients.users.private_users_client import User
from testdata.files.files_client import File


class GetCoursesRequestDict(TypedDict):
    """
    Описание структуры запроса на получение списка курсов.
    """
    userId: int

class CreateCoursesRequestDict(TypedDict):
    """
    Описание структуры запроса на создание курса.
    """
    title: str
    maxScore: int
    minScore: int
    description: str
    estimatedTime: str
    previewFileId: str
    createdByUserId: str

class Course(TypedDict):
    """
    Описание структуры курса.
    """
    id: str
    title: str
    maxScore: int
    minScore: int
    description: str
    previewFile: File
    estimatedTime: str
    createdByUser: User


class CreateCoursesResponse(TypedDict):
    """
    Описание структуры ответа создания курса.
    """
    course: Course


class UpdateCoursesRequestDict(TypedDict):
    """
    Описание структуры запроса на обновление курса.
    """

    title: str
    maxScore: int
    minScore: int
    description: str
    estimatedTime: str


class CoursesClient(ApiClient):
    """
    Клиент для работы с /api/v1/courses
    """

    def get_courses_api(self, query: GetCoursesRequestDict) -> Response:
        """
        Метод получения списка курсов.
        :param query: Словарь с userId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get("/api/v1/courses", params=query)

    def get_course_api(self, course_id: int) -> Response:
        """
        Метод получения курса.
        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"/api/v1/courses/{course_id}")

    def create_course_api(self, request: CreateCoursesRequestDict) -> Response:
        """
        Метод создания курса.
        :param request: Словарь с title, maxScore, minScore, description, estimatedTime,
        previewFileId, createdByUserId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post("/api/v1/courses", json=request)

    def create_course(self, request: CreateCoursesRequestDict) -> CreateCoursesResponse:
        response = self.create_course_api(request)
        return response.json()

    def update_course_api(self, course_id: int, request: UpdateCoursesRequestDict) -> Response:
        """
        Метод обновления курса.
        :param course_id: Идентификатор курса.
        :param request: Словарь с title, maxScore, minScore, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch(f"/api/v1/courses/{course_id}", json=request)

    def delete_course_api(self, course_id: int) -> Response:
        """
        Метод удаления курса.
        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f"/api/v1/courses/{course_id}")

def get_private_course_client(user: AuthenticationUserDict) -> CoursesClient:
    return CoursesClient(client=get_private_http_builder(user))