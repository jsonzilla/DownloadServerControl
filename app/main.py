from app.routes.v1.admin import access_route, block_route, version_route, user_route
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.core.config import settings
from app.core.security import get_token_header
from app.storages.database_storage import close_db, connect_db
from app.routes.v1 import root_route


def get_application():
    """Create a new FastAPI application."""
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description=settings.PROJECT_DESCRIPTION,
        dependencies=[Depends(get_token_header)]
    )
    if (settings.ENABLE_ADMIN):
        _app.include_router(access_route.router)
        _app.include_router(block_route.router)
        _app.include_router(user_route.router)
        _app.include_router(version_route.router)

    _app.include_router(root_route.router)
    return _app


def get_complete_application():
    """In prodution need to start and close db connection and some middleware."""
    _app = get_application()
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.add_middleware(GZipMiddleware, minimum_size=1000)
    _app.add_event_handler("startup", connect_db)
    _app.add_event_handler("shutdown", close_db)
    return _app


app = get_complete_application()
