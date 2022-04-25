from typing import Any, Generator
from app.core.config import settings
from app.models.examples.user_example import another_example, basic_request_example
from app.storages.database_storage import Database
from app.repositories import UserRepository

from bson import objectid
import pytest_asyncio

valid_json = another_example


@pytest_asyncio.fixture
async def id(db: Database) -> Generator[str, Any, None]:
    repo = UserRepository()
    valid_json['_id'] = objectid.ObjectId().__str__()
    id = await repo.insert(valid_json, db)
    yield id
    await db[repo.table_name].drop()


def test_write_users(client, basicAuthHash):
    response = client.post(
        '/v1/user/',
        headers={
            'Content-Type': 'application/json',
            'Authorization': basicAuthHash,
            'x-token': settings.API_TOKEN,
        },
        json=basic_request_example)
    assert response.json()
    assert response.status_code == 201


def test_read_users(client, basicAuthHash):
    response = client.get('/v1/user/',
                          headers={
                              'Authorization': basicAuthHash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 200
    assert not response.json() == {}


def test_read_users_by_fake_id(client, basicAuthHash):
    response = client.get('/v1/user/fake',
                          headers={
                              'Authorization': basicAuthHash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 404
    assert not response.json() == {}


def test_read_users_by_id(client, id, basicAuthHash):
    response = client.get(f'/v1/user/{id}',
                          headers={
                              'Authorization': basicAuthHash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 200
    assert not response.json() == {}


def test_try_update_users_without_data(client, id, basicAuthHash):
    response = client.put(f'/v1/user/{id}',
                          headers={
                              'Authorization': basicAuthHash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 422
    assert not response.json() == {}


def test_update_users(client, id, basicAuthHash):
    response = client.put(
        f'/v1/user/{id}',
        headers={
            'Content-Type': 'application/json',
            'Authorization': basicAuthHash,
            'x-token': settings.API_TOKEN,
        },
        json=basic_request_example)
    assert response.status_code == 200
    assert not response.json() == {}


def test_delete_users_fake(client, basicAuthHash):
    response = client.delete('/v1/user/fake',
                             headers={
                                 'Authorization': basicAuthHash,
                                 'x-token': settings.API_TOKEN
                             })
    assert response.status_code == 404
    assert not response.json() == {}


def test_delete_users(client, id, basicAuthHash):
    response = client.delete(f'/v1/user/{id}',
                             headers={
                                 'Authorization': basicAuthHash,
                                 'x-token': settings.API_TOKEN
                             })
    assert response.status_code == 204
