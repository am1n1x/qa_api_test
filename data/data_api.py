from api.requests.models import EntityRequest, AdditionRequest

def create_entity_payload(
        title="Default Test Title",
        verified=True,
        info="Default additional info",
        number=100,
        important_numbers=[1, 2, 3]
) -> EntityRequest:
    """Генерирует объект EntityRequest с тестовыми данными."""
    return EntityRequest(
        addition=AdditionRequest(
            additional_info=info,
            additional_number=number
        ),
        important_numbers=important_numbers,
        title=title,
        verified=verified
    )
