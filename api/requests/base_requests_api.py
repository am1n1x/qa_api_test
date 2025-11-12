import requests
from requests import Response
from .models import EntityRequest

class EntityApiClient:
    """Клиент для взаимодействия с API сущностей."""
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers = {'Content-Type': 'application/json'}

    def create_entity(self, payload: EntityRequest) -> Response:
        """POST /api/create - Создание сущности."""
        return requests.post(
            url=f"{self.base_url}/api/create",
            data=payload.model_dump_json(),
            headers=self.headers
        )

    def get_entity(self, entity_id: int) -> Response:
        """GET /api/get/{id} - Получение сущности."""
        return requests.get(url=f"{self.base_url}/api/get/{entity_id}")

    def get_all_entities(self) -> Response:
        """GET /api/getAll - Получение всех сущностей."""
        return requests.get(url=f"{self.base_url}/api/getAll")

    def update_entity(self, entity_id: int, payload: EntityRequest) -> Response:
        """PATCH /api/patch/{id} - Обновление сущности."""
        return requests.patch(
            url=f"{self.base_url}/api/patch/{entity_id}",
            data=payload.model_dump_json(),
            headers=self.headers
        )

    def delete_entity(self, entity_id: int) -> Response:
        """DELETE /api/delete/{id} - Удаление сущности."""
        return requests.delete(url=f"{self.base_url}/api/delete/{entity_id}")