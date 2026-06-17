from pydantic import BaseModel, Field, ConfigDict
from tools.fakers import fake

class ExerciseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str
    title: str
    course_id: str = Field(alias='courseId')
    max_score: int = Field(alias='maxScore')
    min_score: int = Field(alias='minScore')
    order_index: int = Field(alias='orderIndex')
    description: str
    estimated_time: str = Field(alias='estimatedTime')

class GetExerciseResponseSchema(BaseModel):
    exercise: ExerciseSchema

class GetExercisesQuerySchema(BaseModel):
    """
    Словарь параметров для запроса списка упражнений.
    Содержит обязательный ключ 'courseId' для фильтрации по курсу.
    Формат: {"courseId": "строка-uuid"}
    """
    model_config = ConfigDict(populate_by_name=True)
    course_id: str = Field(alias='courseId')

class GetExercisesResponseSchema(BaseModel):
    exercises: list[ExerciseSchema]

class CreateExerciseRequestSchema(BaseModel):
    """
    Структура тела запроса для создания упражнения.
    Обязательные поля: title, courseId, description.
    Опциональные поля (могут иметь значение None): maxScore, minScore, orderIndex, estimatedTime.
    Ключи должны присутствовать в словаре; None используется для передачи null на сервер.
    """
    model_config = ConfigDict(populate_by_name=True)
    title: str = Field(default_factory=fake.sentence)
    course_id: str = Field(alias='courseId', default_factory=fake.uuid)
    max_score: int | None = Field(alias='maxScore', default_factory=fake.max_score)
    min_score: int | None = Field(alias='minScore', default_factory=fake.min_score)
    order_index: int | None = Field(alias='orderIndex', default_factory=fake.integer)
    description: str = Field(default_factory=fake.text)
    estimated_time: str | None = Field(alias='estimatedTime', default_factory=fake.estimate_time)

class CreateExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа создания задания.
    """
    exercise: ExerciseSchema

class UpdateExerciseRequestSchema(BaseModel):
    """
    Структура тела запроса для полного обновления упражнения (PATCH).
    Все поля обязательны к передаче: title, maxScore, minScore, orderIndex, description, estimatedTime.
    Тип значений: строки и целые числа (без None).
    """
    model_config = ConfigDict(populate_by_name=True)
    title: str = Field(default_factory=fake.sentence)
    max_score: int = Field(alias='maxScore', default_factory=fake.max_score)
    min_score: int = Field(alias='minScore', default_factory=fake.min_score)
    order_index: int = Field(alias='orderIndex', default_factory=fake.integer)
    description: str = Field(default_factory=fake.text)
    estimated_time: str = Field(alias='estimatedTime', default_factory=fake.estimate_time)

class UpdateExerciseResponseSchema(BaseModel):
    exercise: ExerciseSchema
