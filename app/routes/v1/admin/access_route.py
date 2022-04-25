from typing import List
from fastapi import APIRouter, Depends
from app.repositories.access_repository import AccessRepository
from app.models import AccessModel
from app.storages.database_storage import get_db
from app.core.security import validate_auth
from app.routes import BasicRouter


_name = "access"
router = APIRouter(
    prefix=f"/v1/{_name}",
    tags=[_name],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(validate_auth)]
)
_repo = AccessRepository()
_impl = BasicRouter(_repo, _name)


@router.get("/", response_description=f"List all {_name}s", response_model=List[AccessModel])
async def list(db=Depends(get_db)):
    return await _impl.get_all(db)
