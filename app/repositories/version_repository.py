from app.repositories.base_repository import BaseRepository


class VersionRepository(BaseRepository):
    def __init__(self):
        super().__init__('version')
