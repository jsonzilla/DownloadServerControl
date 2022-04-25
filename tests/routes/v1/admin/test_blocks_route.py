from typing import Any, Generator
from app.core.config import settings
from app.models.examples.block_example import example as valid_json
from app.storages.database_storage import Database
from app.repositories import BlockRepository

from bson import objectid
import pytest_asyncio


@pytest_asyncio.fixture
async def id(db: Database) -> Generator[str, Any, None]:
    repo = BlockRepository()
    valid_json['_id'] = objectid.ObjectId().__str__()
    id = await repo.insert(valid_json, db)
    yield id
    await db[repo.table_name].drop()


def test_write_block(client, basicAuthHash):
    response = client.post(
        '/v1/block/',
        headers={
            'Content-Type': 'application/json',
            'Authorization': basicAuthHash,
            'x-token': settings.API_TOKEN,
        },
        json=valid_json)
    assert response.status_code == 201


def test_read_block(client, basicAuthHash):
    response = client.get('/v1/block/',
                          headers={
                              'Authorization': basicAuthHash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 200
    assert not response.json() == {}


def test_read_block_by_kafe_id(client, basicAuthHash):
    response = client.get('/v1/block/fake',
                          headers={
                              'Authorization': basicAuthHash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 404
    assert not response.json() == {}


def test_read_block_by_id(client, id, basicAuthHash):
    response = client.get(f'/v1/block/{id}',
                          headers={
                              'Authorization': basicAuthHash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 200
    assert not response.json() == {}


def test_update_block_without_content(client, id, basicAuthHash):
    response = client.put(f'/v1/block/{id}',
                          headers={
                              'Authorization': basicAuthHash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 422
    assert not response.json() == {}


def test_update_block(client, id, basicAuthHash):
    response = client.put(
        f'/v1/block/{id}',
        headers={
            'Content-Type': 'application/json',
            'Authorization': basicAuthHash,
            'x-token': settings.API_TOKEN,
        },
        json=valid_json)
    assert response.status_code == 200
    assert not response.json() == {}


def test_delete_block_fake_id(client, basicAuthHash):
    response = client.delete('/v1/block/fake',
                             headers={
                                 'Authorization': basicAuthHash,
                                 'x-token': settings.API_TOKEN
                             })
    assert response.status_code == 404
    assert not response.json() == {}


def test_delete_block(client, id, basicAuthHash):
    response = client.delete(f'/v1/block/{id}',
                             headers={
                                 'Authorization': basicAuthHash,
                                 'x-token': settings.API_TOKEN
                             })
    assert response.status_code == 204
