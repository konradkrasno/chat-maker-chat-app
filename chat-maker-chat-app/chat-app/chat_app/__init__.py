from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chat_app.dao import Dao

app = FastAPI()
# TODO implement Dependency Injection mechanism
dao = Dao("files")
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from chat_app.http import routes
from chat_app.websocket import routes
