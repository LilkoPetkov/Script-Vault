from typing import List

from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from auth.user_auth import get_current_active_user, user_is_admin
from auth.user_auth import oauth2_scheme
from crud_functions.scripts_crud import add_script, delete_script, read_scripts, path_update, assing_script, \
    user_scripts, search_specific_script, find_script_crud, remove_script_from_user_crud
from database.db import get_db
from models.script_model import Script
from schemas.request_schemas.user_request_schemas import UserRequestSchema
from schemas.response_schemas.script_response_schema import AdminScriptResponseSchema, ScriptsMeResponseSchema
from schemas.response_schemas.user_response_schema import UserMeResponseSchema

router = APIRouter(
    prefix="/scripts",
    tags=["Scripts"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}}
)


# Get user script
@router.get("/call/{script_id}")
async def call_script(
        script_id: int,
        current_user: Annotated[UserMeResponseSchema, Depends(get_current_active_user)],
        db: Session = Depends(get_db)
):
    file_path = find_script_crud(db=db, script_id=script_id, user_id=current_user.user_id)
    script = db.query(Script).filter(Script.script_id == script_id).first()

    return FileResponse(
        path=file_path,
        headers={"X-Script": script.name},
        filename=script.name
    )


# Display all user scripts
@router.get("/me", response_model=List[ScriptsMeResponseSchema])
async def read_scripts_me(
        current_user: Annotated[UserMeResponseSchema, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
) -> object:
    return user_scripts(current_user=current_user)


# See all scripts - Admin
@router.get("/all", response_model=List[AdminScriptResponseSchema])
async def all_scripts(
        user: Annotated[UserRequestSchema, Depends(user_is_admin)],
        db: Session = Depends(get_db)
) -> object:
    return read_scripts(db=db)


# Search for specific script - Admin
@router.get("/script/{script_id}", response_model=AdminScriptResponseSchema)
async def search_script(
        script_id: int,
        user: Annotated[UserRequestSchema, Depends(user_is_admin)],
        db: Session = Depends(get_db)
) -> dict:
    return search_specific_script(db=db, script_id=script_id)


# Add script - Admin
@router.post("/add-scipt", response_model=AdminScriptResponseSchema, status_code=200)
async def add_new_script(
        user: Annotated[UserRequestSchema, Depends(user_is_admin)],
        file: UploadFile,
        db: Session = Depends(get_db),
) -> object:
    return add_script(db=db, file=file)


# Update path - Admin
@router.patch("/update-path", response_model=List[AdminScriptResponseSchema])
async def update_path(
        user: Annotated[UserRequestSchema, Depends(user_is_admin)],
        db: Session = Depends(get_db)
) -> object:
    return path_update(db=db)


# Assign script to user
@router.post("/assign-script/{script_id}/{user_id}")
async def assign_script(
        script_id: int,
        user_id: int,
        user: Annotated[UserRequestSchema, Depends(user_is_admin)],
        db: Session = Depends(get_db)
) -> dict:
    return assing_script(db=db, script_id=script_id, user_id=user_id)


# Remove script from user
@router.delete("/delete/{script_id}/{user_id}")
async def remove_script_from_user(
        script_id: int,
        user_id: int,
        user: Annotated[UserRequestSchema, Depends(user_is_admin)],
        db: Session = Depends(get_db)
) -> dict:
    return remove_script_from_user_crud(db=db, script_id=script_id, user_id=user_id)


# Delete script - Admin
@router.delete("/delete/{script_id}", status_code=200)
async def remove_script_completely(
        script_id: int,
        user: Annotated[UserRequestSchema, Depends(user_is_admin)],
        db: Session = Depends(get_db)
) -> object:
    return delete_script(db=db, script_id=script_id)
