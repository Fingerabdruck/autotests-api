from typing import TypedDict
from httpx import Response
from clients.api_client import ApiClient
from clients.private_http_builder import get_private_http_builder, AuthenticationUserDict


class CreateFileRequestDict(TypedDict):
    """
    Описание структуры запроса на создание файла.
    """
    filename: str
    directory: str
    upload_file: str

class File(TypedDict):
    """
    Описание структуры файла.
    """
    id: str
    filename: str
    directory: str
    url: str

class CreateFileResponse(TypedDict):
    """
    Описание структуры ответа создания файла.
    """
    file: File


class FilesClient(ApiClient):
    """
    Клиент для работы с /api/v1/files
    """
    def get_file_api(self, file_id: str) -> Response:
        """
        Метод получения файла.
        :param file_id: Идентификатор файла.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"/api/v1/files/{file_id}")

    def create_file_api(self, request: CreateFileRequestDict) -> Response:
        """
        Метод создания файла.
        :param request: Словарь с filename, directory, upload_file.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(f"/api/v1/files", data=request, files = {"upload_file": open('./testdata/files/image.png', 'rb')},)

    def create_file(self, request: CreateFileRequestDict) -> CreateFileResponse:
        response = self.create_file_api(request)
        return response.json()

    def delete_file_api(self, file_id: str) -> Response:
        """
        Метод удаления файла.
        :param file_id: Идентификатор файла.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f"/api/v1/files/{file_id}")

def get_private_file_client(user: AuthenticationUserDict) -> FilesClient:
    return FilesClient(client=get_private_http_builder(user))