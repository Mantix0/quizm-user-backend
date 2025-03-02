import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from .users.router import router as router_users
from .database import *
app = FastAPI()
app.include_router(router_users)

