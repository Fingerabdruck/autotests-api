import allure

from clients.api_client import ApiClient
from httpx import Response

from clients.exercises.exercises_schema import GetExercisesQuerySchema, GetExercisesResponseSchema, \
    CreateExerciseRequestSchema, CreateExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema
from clients.private_http_builder import get_private_http_builder,  AuthenticationUserSchema
from tools.routes import APIRoutes


class ExercisesClient(ApiClient):
    """
    Клиент для работы с эндпоинтами упражнений.
    Предоставляет методы для получения, создания, обновления и удаления упражнений через API.
    Наследуется от ApiClient, использует httpx под капотом.
    """

    @allure.step("Get Exercises")
    def get_exercises_api(self, query: GetExercisesQuerySchema) -> Response:
        """
        Получает список упражнений, отфильтрованных по идентификатору курса.
        Назначение: выборка упражнений конкретного курса.
        :param query: Словарь с обязательным ключом 'courseId' (str) — ID курса для фильтрации.
        :return: Объект ответа сервера (httpx.Response); содержит JSON со списком упражнений при успехе.
        """
        return self.get(APIRoutes.EXERCISES, params=query.model_dump(by_alias=True))

    def get_exercises(self, query: GetExercisesQuerySchema) -> GetExercisesResponseSchema:
        response = self.get_exercises_api(query)
        return GetExercisesResponseSchema.model_validate_json(response.text)

    @allure.step("Get Exercise")
    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Получает данные конкретного упражнения по его уникальному идентификатору.
        Назначение: получение детальной информации об одном упражнении.
        :param exercise_id: Строка (str) с UUID упражнения, данные которого требуется получить.
        :return: Объект ответа сервера (httpx.Response); содержит JSON с данными упражнения при успехе.
        """
        return self.get(f"{APIRoutes.EXERCISES}/{exercise_id}")

    def get_exercise(self, exercise_id: str) -> GetExercisesResponseSchema:
        response = self.get_exercise_api(exercise_id)
        return GetExercisesResponseSchema.model_validate_json(response.text)

    @allure.step("Create Exercise")
    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        """
        Создаёт новое упражнение в системе.
        Назначение: добавление упражнения с заданными параметрами.
        :param request: Словарь данных (CreateExerciseRequestDict). Должен содержать title, courseId и description;
        поля maxScore, minScore, orderIndex и estimatedTime могут быть None.
        :return: Объект ответа сервера (httpx.Response); при успехе содержит данные созданного упражнения и статус 201.
        """
        return self.post(APIRoutes.EXERCISES, json=request.model_dump(by_alias=True))

    def create_exercise(self, request: CreateExerciseRequestSchema) -> CreateExerciseResponseSchema:
        response = self.create_exercise_api(request)
        return CreateExerciseResponseSchema.model_validate_json(response.text)

    @allure.step("Update Exercise")
    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> Response:
        """
        Обновляет данные существующего упражнения (частичное обновление через PATCH).
        Назначение: изменение параметров упражнения по его ID.
        :param exercise_id: Строка (str) с UUID обновляемого упражнения.
        :param request: Словарь новых данных (UpdateExerciseRequestDict); все поля (title, maxScore, minScore,
        orderIndex, description, estimatedTime) обязательны к передаче.
        :return: Объект ответа сервера (httpx.Response); при успехе содержит обновлённые данные упражнения.
        """
        return self.patch(f"{APIRoutes.EXERCISES}/{exercise_id}", json=request.model_dump(by_alias=True))

    def update_exercise(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> UpdateExerciseResponseSchema:
        response = self.update_exercise_api(exercise_id, request)
        return UpdateExerciseResponseSchema.model_validate_json(response.text)

    @allure.step("Delete Exercise")
    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Удаляет упражнение из системы по его идентификатору.
        Назначение: безвозвратное удаление упражнения.
        :param exercise_id: Строка (str) с UUID удаляемого упражнения.
        :return: Объект ответа сервера (httpx.Response); при успехе обычно имеет статус 204 (No Content) или
        содержит подтверждение удаления.
        """
        return self.delete(f"/api/v1/exercises/{exercise_id}")

def get_exercise_client(user: AuthenticationUserSchema ) -> ExercisesClient:
    """
    Функция создаёт экземпляр ExercisesClient с уже настроенным HTTP-клиентом.
    :return: Готовый к использованию ExercisesClient.
    """
    return ExercisesClient(client=get_private_http_builder(user))