from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

import api.auth.user as auth_cruds
from api.db import get_db

from typing import List
import api.schemes.auth as auth_schema
from api.auth.user import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/auth/register")
async def register_new_account(
    auth_body : auth_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    success = await auth_cruds.create_user(db, auth_body)
    if not success:
        raise HTTPException(status_code=404, detail="Register user failed")
    return {"message" : "user created."}

@router.post("/auth/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> auth_schema.Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    content = {"access_token":access_token, "type":"barer"}
    response = JSONResponse(content=content)
    response.set_cookie(key="access_token", value=access_token, httponly=True, path="/")
    return response

@router.get("/auth/logout")
async def logout_user():
    response = JSONResponse(content={"message": "Successfully logged out"})
    response.delete_cookie(key="access_token", path="/")
    return response