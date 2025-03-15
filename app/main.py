import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from .users.router import router as router_users, router_records
from .database import *

app = FastAPI()
app.include_router(router_users)
app.include_router(router_records)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(404)
async def custom_404_handler(_, __):
    data = {
        "data": "null",
        "errors": [
            {"code": "NotFoundHttpException", "message": "Страница не существует"}
        ],
    }
    json_data = jsonable_encoder(data)
    return JSONResponse(json_data)
