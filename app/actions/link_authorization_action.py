from typing import Optional
from enum import Enum
from datetime import datetime
from pydantic import IPvAnyAddress
from fastapi.encoders import jsonable_encoder
from app.models import AccessModel, VersionModel, VersionRequestModel
from app.repositories import AccessRepository, BlockRepository, VersionRepository
from app.storages.database_storage import get_db


class BindingErrors(str, Enum):
    NONE = 'none'
    VERSION_NOT_FOUND = 'Version not found'
    VERSION_ALREADY_RELEASED = 'This version is already released'
    ACCESS_DENIES = 'Access denied'


class LinkAuthorizationBinding(object):
    def __init__(self) -> None:
        self._access_repo = AccessRepository()
        self._block_repo = BlockRepository()
        self._version_repo = VersionRepository()

    async def get_link(self, client_host, version_request: VersionRequestModel, db):
        if await self._is_blocked(version_request, db):
            return (BindingErrors.ACCESS_DENIES, None)

        last_version = await self._get_last_version(version_request, db)
        if not last_version:
            return (BindingErrors.VERSION_NOT_FOUND, None)

        if last_version['program']['release'] == version_request.program.release:
            return (BindingErrors.VERSION_ALREADY_RELEASED, None)

        await self._save_access(version_request, client_host, last_version, db)

        return (BindingErrors.NONE, {'url': last_version['link']})

    async def _get_last_version(self, version: VersionRequestModel, db) -> Optional[VersionModel]:
        above_versions = await self._version_repo.get_by_and_sort(
            {
                'program.application_name': version.program.application_name,
                'program.revision': {'$gt': version.program.revision},
                'program.protection': version.program.protection,
                'program.language': version.program.language,
                'program.subscription': version.program.subscription
            },
            'program.revision',
            db)
        if len(above_versions) == 0:
            return None
        return above_versions[0]

    async def _is_blocked(self, version: VersionRequestModel, db) -> bool:
        block_list = await self._block_repo.get_one(
            {
                'program.application_name': version.program.application_name,
                'program.revision': version.program.revision,
                'program.release': version.program.release,
                'program.protection': version.program.protection,
                'program.language': version.program.language,
                'program.subscription': version.program.subscription
            }, db)

        return block_list is not None

    async def _save_access(
        self,
        version_request: VersionRequestModel,
        client_host: IPvAnyAddress,
        lastest: VersionModel,
        db: get_db
    ) -> None:
        acessed = AccessModel(
            client_id=version_request.client_id,
            client_host=client_host,
            date_time=datetime.utcnow().timestamp(),
            program_request=version_request.program,
            program_response=lastest['program'],
        )
        element = jsonable_encoder(acessed)
        await self._access_repo.insert(element, db)
