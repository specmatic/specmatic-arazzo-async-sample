import pathlib
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlmodel import Session, SQLModel, create_engine

from location_api.config import Config
from location_api.models import User

config = Config()  # pyright: ignore[reportCallIssue]
connect_args = {"check_same_thread": False}
engine = create_engine(config.LOCATION_DATABASE_URI, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    users = [
        User(id=1, email="specmatic@test.com", password="specmatic", shipping_zone="A", country="IN", region="HYD"),  # noqa: S106
        User(id=2, email="another@user.com", password="user", shipping_zone="B", country="IN", region="DEL"),  # noqa: S106
    ]
    with Session(engine) as session:
        session.add_all(users)
        session.commit()


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ValidationError)
@app.exception_handler(RequestValidationError)
def handle_validation_error(_, e: "RequestValidationError|ValidationError"):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Bad Request",
            "message": str(e),
        },
    )


@app.exception_handler(HTTPException)
def http_error_handler(_, e: "HTTPException"):
    return JSONResponse(
        status_code=e.status_code,
        content={
            "error": e.__class__.__name__,
            "message": e.detail,
        },
    )


from .routes import auth_location_router  # noqa: E402

app.include_router(auth_location_router)
