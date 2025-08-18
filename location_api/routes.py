from uuid import uuid4

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from location_api import SessionDep
from location_api.models import LocationRequest, LocationResponse, User

auth_location_router = APIRouter()


@auth_location_router.post("/location", response_model=LocationResponse)
async def get_uuids(request_data: LocationRequest, session: SessionDep):
    statement = select(User).where(User.email == request_data.email)
    user = session.exec(statement).one()

    if not user or user.password != request_data.password:
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    client_token = uuid4().hex
    return LocationResponse.model_validate({**user.model_dump(), "client_token": client_token})
