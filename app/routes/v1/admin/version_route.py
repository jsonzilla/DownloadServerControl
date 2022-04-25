from typing import List
from fastapi import APIRouter, Depends
from fastapi import Body
from app.core.security import validate_auth
from app.storages.database_storage import get_db
from app.models import VersionModel, UpdateVersionModel
from app.repositories import VersionRepository
from app.routes import BasicRouter

_name = "version"
router = APIRouter(
    prefix=f"/v1/{_name}",
    tags=[_name],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(validate_auth)]
)
_repo = VersionRepository()
_impl = BasicRouter(_repo, _name)


@router.post("/", response_description=f"Add new {_name}", response_model=VersionModel)
async def create(version: VersionModel = Body(...), db=Depends(get_db)):
    return await _impl.post(version, db)


@router.get("/", response_description=f"List all {_name}s", response_model=List[VersionModel])
async def lists(db=Depends(get_db)):
    return await _impl.get_all(db)


@router.get("/{id}", response_description=f"Get a single {_name}", response_model=VersionModel)
async def show(id: str, db=Depends(get_db)):
    return await _impl.get_by_id(id, db)


@router.put("/{id}", response_description=f"Update a {_name}", response_model=VersionModel)
async def update(id: str, version: UpdateVersionModel = Body(...), db=Depends(get_db)):
    return await _impl.put(id, version, db)


@router.delete("/{id}", response_description=f"Delete a {_name}")
async def delete(id: str, db=Depends(get_db)):
    return await _impl.delete(id, db)
