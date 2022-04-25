from typing import Any, Generator
from app.core.config import settings
from app.models.examples.version_example import example as valid_json
from app.storages.database_storage import Database
from app.repositories import VersionRepository

from bson import objectid
import pytest_asyncio


@pytest_asyncio.fixture
async def id(db: Database) -> Generator[str, Any, None]:
    repo = VersionRepository()
    valid_json['_id'] = objectid.ObjectId().__str__()
    id = await repo.insert(valid_json, db)
    yield id
    await db[repo.table_name].drop()


def test_write_version(client, basicAuthHash):
    response = client.post(
        '/v1/version/',
        headers={
            'Content-Type': 'application/json',
            'Authorization': basicAuthHash,
            'x-token': settings.API_TOKEN,
        },
        json=valid_json)
    assert response.status_code == 201


def test_read_version(client, basicAuthHash):
    response = client.get('/v1/version/',
                          headers={
                              'Authorization': basicAuthHash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 200
    assert not response.json() == {}


def test_read_version_by_fake_id(client, basicAuthHash):
    response = client.get('/v1/version/fake',
                          headers={
                              'Authorization': basicAuthHash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 404
    assert not response.json() == {}


def test_read_version_by_id(client, id, basicAuthHash):
    response = client.get(f'/v1/version/{id}',
                          headers={
                              'Authorization': basicAuthHash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 200
    assert not response.json() == {}


def test_update_version_without_body(client, id, basicAuthHash):
    response = client.put(f'/v1/version/{id}',
                          headers={
                              'Authorization': basicAuthHash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 422
    assert not response.json() == {}


def test_update_version_fake_id(client, basicAuthHash):
    response = client.put(
        '/v1/version/fake',
        headers={
            'Content-Type': 'application/json',
            'Authorization': basicAuthHash,
            'x-token': settings.API_TOKEN,
        },
        json={'description': 'paypal'})
    assert response.status_code == 404
    assert not response.json() == {}


def test_update_version(client, id, basicAuthHash):
    response = client.put(
        f'/v1/version/{id}',
        headers={
            'Content-Type': 'application/json',
            'Authorization': basicAuthHash,
            'x-token': settings.API_TOKEN,
        },
        json={'description': 'paypal'})
    assert response.status_code == 200
    assert not response.json() == {}


def test_delete_version_with_fake_id(client, basicAuthHash):
    response = client.delete(
        '/v1/version/fake',
        headers={
            'Authorization': basicAuthHash,
            'x-token': settings.API_TOKEN
        })
    assert response.status_code == 404
    assert response.json() == {'detail': 'version fake not found'}


def test_delete_version(client, id, basicAuthHash):
    response = client.delete(f'/v1/version/{id}',
                             headers={
                                 'Authorization': basicAuthHash,
                                 'x-token': settings.API_TOKEN
                             })
    assert response.status_code == 204


def test_write_version_without_x_token(client, basicAuthHash):
    response = client.post(
        '/v1/version/',
        headers={
            'Content-Type': 'application/json',
            'Authorization': basicAuthHash,
        },
        json=valid_json)
    assert response.status_code == 422


def test_write_version_without_auth(client, basicAuthHash):
    response = client.post(
        '/v1/version/',
        headers={
            'Content-Type': 'application/json',
            'x-token': settings.API_TOKEN
        },
        json=valid_json)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}
