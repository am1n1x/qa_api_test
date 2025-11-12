from pydantic import BaseModel
from typing import List


class AdditionRequest(BaseModel):
    """Модель для дополнительной информации в запросе."""
    additional_info: str
    additional_number: int


class EntityRequest(BaseModel):
    """Модель для создания/обновления сущности."""
    addition: AdditionRequest
    important_numbers: List[int]
    title: str
    verified: bool


class AdditionResponse(BaseModel):
    """Модель для дополнительной информации в ответе."""
    id: int
    additional_info: str
    additional_number: int


class EntityResponse(BaseModel):
    """Модель для ответа при получении сущности."""
    id: int
    addition: AdditionResponse
    important_numbers: List[int]
    title: str
    verified: bool
