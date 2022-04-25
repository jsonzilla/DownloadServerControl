from app.repositories.base_repository import BaseRepository


class AccessRepository(BaseRepository):
    def __init__(self):
        super().__init__('access')
