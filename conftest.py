import pytest
import os
from dotenv import load_dotenv
from api.requests.base_requests_api import EntityApiClient
from data.data_api import create_entity_payload

load_dotenv()

@pytest.fixture(scope="session")
def api_client() -> EntityApiClient:
    """Фикстура для создания экземпляра API клиента."""
    base_url = os.getenv("BASE_URL")
    if not base_url:
        raise ValueError("BASE_URL не найден в .env файле")
    return EntityApiClient(base_url=base_url)


@pytest.fixture(scope="function")
def created_entity_id(api_client: EntityApiClient) -> int:
    """
    Фикстура для создания сущности перед тестом и её удаления после.
    """
    payload = create_entity_payload(title="Entity for testing")
    response = api_client.create_entity(payload)
    assert response.status_code == 200, "Не удалось создать сущность для теста"
    entity_id = int(response.text)

    yield entity_id

    api_client.delete_entity(entity_id)
