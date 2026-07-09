import allure
from httpx import Response
from clients.api_client import ApiClient
from clients.private_http_builder import get_private_http_builder, AuthenticationUserSchema
from testdata.files.file_schema import CreateFileRequestSchema, CreateFileResponseSchema
from tools.routes import APIRoutes


class FilesClient(ApiClient):
    """
    Клиент для работы с /api/v1/files
    """

    @allure.step("Get file by id {file_id}")
    def get_file_api(self, file_id: str) -> Response:
        """
        Метод получения файла.
        :param file_id: Идентификатор файла.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"{APIRoutes.FILES}/{file_id}")

    @allure.step("Create file")
    def create_file_api(self, request: CreateFileRequestSchema) -> Response:
        """
        Метод создания файла.
        :param request: Словарь с filename, directory, upload_file.
        :return: Ответ от сервера в виде объекта httpx.Response
        """

        files = {"upload_file": request.upload_file.read_bytes()}

        return self.post(
            APIRoutes.FILES,
            data=request.model_dump(by_alias=True, exclude={'upload_file'}),
            files=files
        )
    def create_file(self, request: CreateFileRequestSchema) -> CreateFileResponseSchema:
        response = self.create_file_api(request)
        return CreateFileResponseSchema.model_validate_json(response.text)

    @allure.step("Delete file by id {file_id}")
    def delete_file_api(self, file_id: str) -> Response:
        """
        Метод удаления файла.
        :param file_id: Идентификатор файла.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f"{APIRoutes.FILES}/{file_id}")

def get_private_file_client(user: AuthenticationUserSchema) -> FilesClient:
    return FilesClient(client=get_private_http_builder(user))