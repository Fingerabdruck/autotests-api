from pydantic import BaseModel, Field, ConfigDict
from clients.users.user_schema import UserSchema
from testdata.files.file_schema import FileSchema


class GetCoursesRequestSchema(BaseModel):
    """
    Описание структуры запроса на получение списка курсов.
    """
    userId: int

class CreateCoursesRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание курса.
    """
    model_config = ConfigDict(populate_by_name=True)
    title: str
    max_score: int = Field(alias='maxScore')
    min_score: int = Field(alias='minScore')
    description: str
    estimated_time: str = Field(alias='estimatedTime')
    preview_file_id: str = Field(alias='previewFileId')
    created_by_user_id: str = Field(alias='createdByUserId')

class CourseSchema(BaseModel):
    """
    Описание структуры курса.
    """
    model_config = ConfigDict(populate_by_name=True)
    id: str
    title: str
    max_score: int = Field(alias='maxScore')
    min_score: int = Field(alias='minScore')
    description: str
    preview_file: FileSchema = Field(alias='previewFile')
    estimated_time: str = Field(alias='estimatedTime')
    created_by_user_id: UserSchema = Field(alias='createdByUser')


class CreateCoursesResponseSchema(BaseModel):
    """
    Описание структуры ответа создания курса.
    """
    course: CourseSchema


class UpdateCoursesRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление курса.
    """
    model_config = ConfigDict(populate_by_name=True)
    title: str
    max_score: int = Field(alias='maxScore')
    min_score: int = Field(alias='minScore')
    description: str
    estimated_time: str = Field(alias='estimatedTime')