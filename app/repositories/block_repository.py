from app.repositories.base_repository import BaseRepository


class BlockRepository(BaseRepository):
    def __init__(self):
        super().__init__('block')
