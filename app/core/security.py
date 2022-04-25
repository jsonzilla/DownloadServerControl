import secrets
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.core import Hasher, settings
from app.repositories import UserRepository
from app.storages.database_storage import get_db

_security = HTTPBasic()


async def get_token_header(x_token: str = Header(...)):
    if x_token != settings.API_TOKEN:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")


async def validate_auth(credentials: HTTPBasicCredentials = Depends(_security), db=Depends(get_db)):
    repo = UserRepository()
    user = await repo.get_one({'username': credentials.username}, db)

    if user:
        correct_username = secrets.compare_digest(credentials.username, user['username'])
        correct_password = Hasher.verify_password(credentials.password, user['password'])

        if (correct_username and correct_password):
            return credentials.username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
