from fastapi import APIRouter, Depends
from fastapi import Body
from typing import List
from app.core.security import validate_auth
from app.storages.database_storage import get_db
from app.models import BlockModel, UpdateBlockModel
from app.repositories import BlockRepository
from app.routes import BasicRouter


_name = "block"
router = APIRouter(
    prefix=f"/v1/{_name}",
    tags=[_name],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(validate_auth)]
)
_repo = BlockRepository()
_impl = BasicRouter(_repo, _name)


@router.post("/", response_description=f"Add new {_name}", response_model=BlockModel)
async def create(version: BlockModel = Body(...), db=Depends(get_db)):
    return await _impl.post(version, db)


@router.get("/", response_description=f"List all {_name}s", response_model=List[BlockModel])
async def list(db=Depends(get_db)):
    return await _impl.get_all(db)


@router.get("/{id}", response_description=f"Get a single {_name}", response_model=BlockModel)
async def show(id: str, db=Depends(get_db)):
    return await _impl.get_by_id(id, db)


@router.put("/{id}", response_description=f"Update a {_name}", response_model=BlockModel)
async def update(id: str, version: UpdateBlockModel = Body(...), db=Depends(get_db)):
    return await _impl.put(id, version, db)


@router.delete("/{id}", response_description=f"Delete a {_name}")
async def delete(id: str, db=Depends(get_db)):
    return await _impl.delete(id, db)
