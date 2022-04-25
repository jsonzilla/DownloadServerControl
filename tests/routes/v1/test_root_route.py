from typing import Any
from mongomock import Database
from pyparsing import Generator
from app.core.config import settings
from app.models.examples.version_example import example, old_release_example, new_release_example
from app.models.examples.version_request_example import example as request_example
from app.models.examples.block_example import example as block_example
from app.repositories import BlockRepository, VersionRepository

from bson import objectid
import pytest_asyncio


@pytest_asyncio.fixture
async def idsVersions(db: Database) -> Generator[str, Any, None]:
    ids = []
    examples = [example, old_release_example, new_release_example]
    repo = VersionRepository()
    for e in examples:
        e['_id'] = objectid.ObjectId().__str__()
        id = await repo.insert(e, db)
        ids.append(id)
    yield ids
    await db[repo.table_name].drop()


@pytest_asyncio.fixture
async def idBlock(db: Database) -> Generator[str, Any, None]:
    repo = BlockRepository()
    block_example['_id'] = objectid.ObjectId().__str__()
    id = await repo.insert(block_example, db)
    yield id
    await db[repo.table_name].drop()


def test_request_a_link_without_a_x_token(client):
    response = client.post("/v1/",
                           headers={
                               "Content-Type": "application/json",
                           },
                           json=example)
    assert response.status_code == 422


def test_request_a_link_with_a_empyt_x_token(client):
    response = client.post("/v1/",
                           headers={
                               "Content-Type": "application/json",
                               "x-token": "",
                           },
                           json=example)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Missing Authorization Header"
    }


def test_request_a_link_without_a_invalid_x_token(client):
    response = client.post("/v1/",
                           headers={
                               "Content-Type": "application/json",
                               "x-token": "I_AM_INVALID",
                           },
                           json=example)
    assert response.status_code == 401


def test_request_a_link_with_invalid_information(client):
    response = client.post("/v1/",
                           headers={"x-token": settings.API_TOKEN})
    assert response.status_code == 422
    assert response.json() == {"detail": [{'loc': ['body'], 'msg': 'field required', 'type': 'value_error.missing'}]}


def test_request_a_link_with_valid_information(client, idsVersions):
    response = client.post("/v1/",
                           headers={
                               "Content-Type": "application/json",
                               "x-token": settings.API_TOKEN,
                           },
                           json=request_example)
    assert response.json() == {'url': new_release_example['link']}
    assert response.status_code == 201


def test_block_request_a_link_with_blocked_version(client, idsVersions, idBlock):
    response = client.post("/v1/",
                           headers={
                               "Content-Type": "application/json",
                               "x-token": settings.API_TOKEN,
                           },
                           json=request_example)
    assert response.json() == {'detail': 'Access denied'}
    assert response.status_code == 403


def test_request_a_link_with_valid_information_but_withou_server_valid_version(client):
    response = client.post("/v1/",
                           headers={
                               "Content-Type": "application/json",
                               "x-token": settings.API_TOKEN,
                           },
                           json=request_example)
    assert response.json() == {'detail': 'Version not found'}
    assert response.status_code == 404
