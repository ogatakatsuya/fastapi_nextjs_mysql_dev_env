from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.routers import auth
from api.routers import posts
from api.routers import reply
from api.routers import profile


app = FastAPI()
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(reply.router)
app.include_router(profile.router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)