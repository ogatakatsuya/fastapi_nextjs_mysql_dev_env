from fastapi import Depends, APIRouter, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

import api.repository.auth.user as auth_cruds
from api.db import get_db
import api.schemes.auth as auth_schema
from api.repository.auth.user import authenticate_user, create_access_token, get_current_user_id, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/auth/register")
async def register_new_account(
    auth_body : auth_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    new_user = await auth_cruds.create_user(db, auth_body.user_name)
    await db.commit()
    await db.refresh(new_user)
    if not new_user:
        raise HTTPException(status_code=500, detail="Register user failed")
    
    password_body = auth_schema.PasswordCreate(user_id=new_user.id, password=auth_body.password)
    new_password = await auth_cruds.create_password(db, password_body)
    await db.commit()
    await db.refresh(new_password)
    if not new_password:
        raise HTTPException(status_code=500, detail="Register password failed")
    return {"message" : "user created."}

@router.post("/auth/login")
async def login_for_access_token(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True, path="/")
    return {"message": "Successfuly login"}

@router.delete("/auth/logout")
async def logout_user(
    response: Response
):
    response.delete_cookie(key="access_token", path="/")
    return {"message": "Successfully log out"}

@router.get("/user")
async def get_user_id(
    db: AsyncSession = Depends(get_db), access_token: str | None = Cookie(default=None)
):
    user_id = await get_current_user_id(db, access_token)
    return user_id