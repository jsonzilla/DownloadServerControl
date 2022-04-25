from fastapi import HTTPException, status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from app.repositories.base_repository import BaseRepository


class BasicRouter(object):
    def __init__(self, repo: BaseRepository, element_name: str = "element"):
        self.repo: BaseRepository = repo
        self.element_name = element_name

    async def post(self, element, db):
        element = jsonable_encoder(element)
        created = await self.repo.create(element, db)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created)

    async def get_all(self, db):
        return await self.repo.get_all(db)

    async def get_by_id(self, id, db):
        if (element := await self.repo.get_by_id(id, db)) is not None:
            return element

        raise HTTPException(status_code=404, detail=f"{self.element_name} {id} not found")

    async def put(self, id, element, db):
        element = {k: v for k, v in element.dict().items() if v is not None}
        if len(element) >= 1:
            update_result = await self.repo.update(id, element, db)

            if update_result.modified_count == 1:
                if (updated := await self.repo.get_by_id(id, db)) is not None:
                    return updated

        if (existing := await self.repo.get_by_id(id, db)) is not None:
            return existing

        raise HTTPException(status_code=404, detail=f"{self.element_name} {id} not found")

    async def delete(self, id, db):
        delete_result = await self.repo.delete(id, db)

        if delete_result.deleted_count == 1:
            return Response(status_code=204)

        raise HTTPException(status_code=404, detail=f"{self.element_name} {id} not found")
