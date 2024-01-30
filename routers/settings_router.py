from fastapi import APIRouter
from schemas.base_schemas.settings_base_schema import Settings

settings = Settings()

router = APIRouter(
    responses={404: {"description": "Not found"}},
    tags=["Settings"]
)


@router.get("/info")
async def info() -> object:
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email
    }
