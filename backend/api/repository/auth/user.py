from datetime import datetime, timedelta, timezone
from typing import Union
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models.models as auth_model
import schemes.auth as auth_schema
from models.models import User, Password

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 900

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_user(db, username: str):
    user = await db.scalar(
        select(User)
        .where(User.name == username)
    )
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_password(db, user_id):
    password = await db.scalar(
        select(Password.password)
        .where(Password.user_id == user_id)
    )
    if password is None:
        raise HTTPException(status_code=404, detail="Password not found")
    return password

async def authenticate_user(db, username: str, password: str):
    user = await get_user(db, username)
    user_password = await get_password(db, user.id)
    if not user:
        return False
    if not verify_password(password, user_password): # passwordが入力されたパスワードでuser_passwordがdbから取ってきた正しいパスワード
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user_id(db: AsyncSession, token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="再度ログインしてください．",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id

async def create_user(db: AsyncSession, user_name: str) -> auth_model.User:
    user = auth_model.User(
        name = user_name
    )
    db.add(user)
    await db.flush()
    return user

async def create_password(db: AsyncSession, password_create: auth_schema.PasswordCreate):
    
    hashed_password = get_password_hash(password_create.password)
    password = auth_model.Password(password=hashed_password, user_id=password_create.user_id)
    db.add(password)
    await db.flush()
    return password