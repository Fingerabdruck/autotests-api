from clients.api_client import ApiClient
from httpx import Response
from typing import TypedDict
from clients.users.private_users_client import User
from clients.private_http_builder import get_private_http_builder,  AuthenticationUserDict
class Exercise(TypedDict):

    id: str
    title: str
    courseId: str
    maxScore: int
    minScore: int
    orderIndex: int
    description: str
    estimatedTime: str

class GetExerciseResponseDict(TypedDict):
    exercise: Exercise

class GetExercisesQueryDict(TypedDict):
    """
    Словарь параметров для запроса списка упражнений.
    Содержит обязательный ключ 'courseId' для фильтрации по курсу.
    Формат: {"courseId": "строка-uuid"}
    """
    courseId: str



class GetExercisesResponseDict(TypedDict):
    exercises: list[Exercise]


class CreateExerciseRequestDict(TypedDict):
    """
    Структура тела запроса для создания упражнения.
    Обязательные поля: title, courseId, description.
    Опциональные поля (могут иметь значение None): maxScore, minScore, orderIndex, estimatedTime.
    Ключи должны присутствовать в словаре; None используется для передачи null на сервер.
    """
    title: str
    courseId: str
    maxScore: int | None
    minScore: int | None
    orderIndex: int | None
    description: str
    estimatedTime: str | None

class UpdateExerciseRequestDict(TypedDict):
    """
    Структура тела запроса для полного обновления упражнения (PATCH).
    Все поля обязательны к передаче: title, maxScore, minScore, orderIndex, description, estimatedTime.
    Тип значений: строки и целые числа (без None).
    """
    title: str
    maxScore: int
    minScore: int
    orderIndex: int
    description: str
    estimatedTime: str


class ExercisesClient(ApiClient):
    """
    Клиент для работы с эндпоинтами упражнений.
    Предоставляет методы для получения, создания, обновления и удаления упражнений через API.
    Наследуется от ApiClient, использует httpx под капотом.
    """

    def get_exercises_api(self, query: GetExercisesQueryDict) -> Response:
        """
        Получает список упражнений, отфильтрованных по идентификатору курса.
        Назначение: выборка упражнений конкретного курса.
        :param query: Словарь с обязательным ключом 'courseId' (str) — ID курса для фильтрации.
        :return: Объект ответа сервера (httpx.Response); содержит JSON со списком упражнений при успехе.
        """
        return self.get("/api/v1/exercises", params=query)

    def get_exercises(self, query: GetExercisesQueryDict) -> GetExercisesResponseDict:
        response = self.get_exercises_api(query)
        return response.json()

    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Получает данные конкретного упражнения по его уникальному идентификатору.
        Назначение: получение детальной информации об одном упражнении.
        :param exercise_id: Строка (str) с UUID упражнения, данные которого требуется получить.
        :return: Объект ответа сервера (httpx.Response); содержит JSON с данными упражнения при успехе.
        """
        return self.get(f"/api/v1/exercises/{exercise_id}")

    def get_exercise(self, exercise_id: str) -> GetExercisesResponseDict:
        response = self.get_exercise_api(exercise_id)
        return response.json()

    def create_exercise_api(self, request: CreateExerciseRequestDict) -> Response:
        """
        Создаёт новое упражнение в системе.
        Назначение: добавление упражнения с заданными параметрами.
        :param request: Словарь данных (CreateExerciseRequestDict). Должен содержать title, courseId и description;
        поля maxScore, minScore, orderIndex и estimatedTime могут быть None.
        :return: Объект ответа сервера (httpx.Response); при успехе содержит данные созданного упражнения и статус 201.
        """
        return self.post("/api/v1/exercises", json=request)

    def create_exercise(self, request: CreateExerciseRequestDict) -> Exercise:
        response = self.create_exercise_api(request)
        return response.json()

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestDict) -> Response:
        """
        Обновляет данные существующего упражнения (частичное обновление через PATCH).
        Назначение: изменение параметров упражнения по его ID.
        :param exercise_id: Строка (str) с UUID обновляемого упражнения.
        :param request: Словарь новых данных (UpdateExerciseRequestDict); все поля (title, maxScore, minScore,
        orderIndex, description, estimatedTime) обязательны к передаче.
        :return: Объект ответа сервера (httpx.Response); при успехе содержит обновлённые данные упражнения.
        """
        return self.patch(f"/api/v1/exercises/{exercise_id}", json=request)

    def update_exercise(self, exercise_id: str, request: UpdateExerciseRequestDict) -> Exercise:
        response = self.update_exercise_api(exercise_id, request)
        return response.json()

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Удаляет упражнение из системы по его идентификатору.
        Назначение: безвозвратное удаление упражнения.
        :param exercise_id: Строка (str) с UUID удаляемого упражнения.
        :return: Объект ответа сервера (httpx.Response); при успехе обычно имеет статус 204 (No Content) или
        содержит подтверждение удаления.
        """
        return self.delete(f"/api/v1/exercises/{exercise_id}")

def get_exercise_client(user: AuthenticationUserDict ) -> ExercisesClient:
    """
    Функция создаёт экземпляр ExercisesClient с уже настроенным HTTP-клиентом.
    :return: Готовый к использованию ExercisesClient.
    """
    return ExercisesClient(client=get_private_http_builder(user))