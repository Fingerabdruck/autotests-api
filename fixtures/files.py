import pytest

from pydantic import BaseModel
from fixtures.user import UserFixture
from testdata.files.file_schema import CreateFileRequestSchema, CreateFileResponseSchema
from testdata.files.files_client import get_private_file_client, FilesClient


class FileFixture(BaseModel):
    request: CreateFileRequestSchema
    response: CreateFileResponseSchema


@pytest.fixture
def files_client(function_user: UserFixture) -> FilesClient:
    return get_private_file_client(function_user.authentication_user)


@pytest.fixture
def function_file(files_client: FilesClient) -> FileFixture:
    request = CreateFileRequestSchema(upload_file='./testdata/files/image.png')
    response = files_client.create_file(request)
    return FileFixture(request=request, response=response)