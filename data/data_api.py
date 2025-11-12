import uuid
from typing import Optional
from api.requests.models import EntityRequest, AdditionRequest


def create_entity_payload(
        title: Optional[str] = None,
        verified: bool = True,
        info: Optional[str] = None,
        number: int = 100,
        important_numbers: list[int] = None
) -> EntityRequest:
    """
    Генерирует объект EntityRequest с тестовыми данными.
    Если title или info не переданы, генерирует уникальные значения.
    """
    unique_id = uuid.uuid4()

    final_title = title if title is not None else f"Test Title {unique_id}"

    final_info = info if info is not None else f"Additional info {unique_id}"

    final_important_numbers = important_numbers if important_numbers is not None else [1, 2, 3]

    return EntityRequest(
        addition=AdditionRequest(
            additional_info=final_info,
            additional_number=number
        ),
        important_numbers=final_important_numbers,
        title=final_title,
        verified=verified
    )
