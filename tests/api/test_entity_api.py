import allure
import json
from pydantic import TypeAdapter
from typing import List

from api.requests.base_requests_api import EntityApiClient
from api.requests.models import EntityResponse
from data.data_api import create_entity_payload

@allure.feature("Управление сущностями (Entity API)")
class TestEntityApi:

    @allure.story("CRUD-операции")
    @allure.title("Создание новой сущности (позитивный сценарий)")
    def test_create_entity(self, api_client: EntityApiClient):
        """Тест на создание сущности: POST /api/create."""
        with allure.step("Подготовка (Arrange): Генерируем тестовые данные для создания сущности"):
            payload = create_entity_payload(title="Unique Title for Create Test")
            allure.attach(
                body=payload.model_dump_json(indent=2),
                name="Тело запроса (Request Body)",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Действие (Act): Отправляем запрос на создание сущности"):
            response = api_client.create_entity(payload)
            entity_id = int(response.text)

        with allure.step("Проверка (Assert): Проверяем статус-код и ID созданной сущности"):
            assert response.status_code == 200
            assert entity_id > 0

        with allure.step("Очистка (Cleanup): Удаляем созданную сущность"):
            api_client.delete_entity(entity_id)


    @allure.story("CRUD-операции")
    @allure.title("Получение созданной сущности по ID")
    def test_get_entity(self, api_client: EntityApiClient, created_entity_id: int):
        """Тест на получение сущности: GET /api/get/{id}."""
        with allure.step("Подготовка (Arrange): ID сущности получен из фикстуры"):
            allure.attach(
                body=str(created_entity_id),
                name="ID запрашиваемой сущности",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Действие (Act): Отправляем запрос на получение сущности"):
            response = api_client.get_entity(created_entity_id)

        with allure.step("Проверка (Assert): Проверяем статус-код и десериализуем данные"):
            assert response.status_code == 200
            entity_data = EntityResponse.model_validate(response.json())
            allure.attach(
                body=json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Тело ответа (Response Body)",
                attachment_type=allure.attachment_type.JSON
            )
            assert entity_data.id == created_entity_id
            assert entity_data.title == "Entity for testing"


    @allure.story("Получение списков")
    @allure.title("Получение списка всех сущностей")
    def test_get_all_entities(self, api_client: EntityApiClient, created_entity_id: int):
        """Тест на получение списка сущностей: GET /api/getAll."""
        with allure.step("Подготовка (Arrange): Создана как минимум одна сущность через фикстуру"):
            pass

        with allure.step("Действие (Act): Отправляем запрос на получение списка сущностей"):
            response = api_client.get_all_entities()

        with allure.step("Проверка (Assert): Проверяем статус-код и наличие нашей сущности в списке"):
            assert response.status_code == 200
            allure.attach(
                body=json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Тело ответа (Response Body)",
                attachment_type=allure.attachment_type.JSON
            )
            list_of_entities = TypeAdapter(List[EntityResponse]).validate_python(response.json()['entity'])
            assert isinstance(list_of_entities, list)
            assert len(list_of_entities) > 0
            assert any(entity.id == created_entity_id for entity in list_of_entities)


    @allure.story("CRUD-операции")
    @allure.title("Обновление существующей сущности")
    def test_update_entity(self, api_client: EntityApiClient, created_entity_id: int):
        """Тест на обновление сущности: PATCH /api/patch/{id}."""
        with allure.step("Подготовка (Arrange): Генерируем новые данные для обновления"):
            updated_payload = create_entity_payload(title="This Title Was Updated", verified=False)
            allure.attach(
                body=updated_payload.model_dump_json(indent=2),
                name="Тело запроса на обновление (Request Body)",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Действие (Act): Отправляем запрос на обновление сущности"):
            response = api_client.update_entity(created_entity_id, updated_payload)

        with allure.step("Проверка (Assert): Проверяем статус-код ответа"):
            assert response.status_code == 204

        with allure.step("Верификация (Verification): Проверяем, что данные действительно обновились"):
            get_response = api_client.get_entity(created_entity_id)
            updated_entity_data = EntityResponse.model_validate(get_response.json())
            allure.attach(
                body=updated_entity_data.model_dump_json(indent=2),
                name="Данные сущности после обновления",
                attachment_type=allure.attachment_type.JSON
            )
            assert updated_entity_data.title == "This Title Was Updated"
            assert updated_entity_data.verified is False


    @allure.story("CRUD-операции")
    @allure.title("Удаление существующей сущности")
    def test_delete_entity(self, api_client: EntityApiClient):
        """Тест на удаление сущности: DELETE /api/delete/{id}."""
        with allure.step("Подготовка (Arrange): Создаем сущность специально для удаления"):
            payload = create_entity_payload(title="Entity To Be Deleted")
            create_response = api_client.create_entity(payload)
            entity_id = int(create_response.text)
            allure.attach(
                body=str(entity_id),
                name="ID созданной для удаления сущности",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Действие (Act): Отправляем запрос на удаление сущности"):
            delete_response = api_client.delete_entity(entity_id)

        with allure.step("Проверка (Assert): Проверяем, что удаление прошло успешно"):
            assert delete_response.status_code == 204

        with allure.step("Верификация (Verification): Проверяем, что сущность больше не доступна"):
            get_response = api_client.get_entity(entity_id)
            assert get_response.status_code != 200
