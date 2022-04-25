from app.storages.database_storage import Database


class BaseRepository(object):
    __slots__ = ['table_name']

    def __init__(self, table_name):
        self.table_name = table_name

    async def create(self, item, db: Database):
        id = await self.insert(item, db)
        return await self.get_by_id(id, db)

    async def insert(self, item, db: Database):
        return (await db[self.table_name].insert_one(item)).inserted_id

    async def get_by_id(self, id, db: Database):
        return await db[self.table_name].find_one({'_id': id})

    async def get_one(self, any, db: Database):
        return await db[self.table_name].find_one(any)

    async def get_by_and_sort(self, any, sort_field, db: Database):
        return await db[self.table_name].find(any).sort(sort_field).to_list(None)

    async def get_all(self, db: Database):
        return await db[self.table_name].find().to_list(None)

    async def update(self, id, item, db: Database):
        return await db[self.table_name].update_one({'_id': id}, {'$set': item})

    async def delete(self, id, db: Database):
        return await db[self.table_name].delete_one({'_id': id})

    async def get_by_and_sort_with_pagination(self, any, sort_field, page, per_page, db: Database):
        return await db[self.table_name].find(any).sort(sort_field).skip(page * per_page).limit(per_page).to_list(None)
