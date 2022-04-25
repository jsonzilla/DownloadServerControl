from fastapi import APIRouter, Body, Depends, HTTPException, status, Request
from app.actions import LinkAuthorizationBinding, BindingErrors
from app.core.security import get_token_header
from app.models import VersionRequestModel
from app.storages.database_storage import get_db

router = APIRouter(
    prefix='/v1',
    tags=['root'],
    responses={404: {'description': 'Not found'}},
    dependencies=[Depends(get_token_header)]
)


@router.post('/', response_description='Obtain download link', status_code=status.HTTP_201_CREATED)
async def get_link(request: Request, version_request: VersionRequestModel = Body(...), db=Depends(get_db)):
    error, link = await LinkAuthorizationBinding().get_link(request.client.host, version_request, db)
    if error == BindingErrors.NONE:
        return link
    elif error == BindingErrors.VERSION_NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error.value)
