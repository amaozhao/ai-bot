from fastapi import APIRouter, HTTPException, status
from ..schemas import JWTToken, SignIn
from ..services import auth_service


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/signin")
async def signin(sigin_schema: SignIn):
    authenticated = await auth_service.authenticate(sigin_schema.username, sigin_schema.password)
    if authenticated:
        return JWTToken(token="abc", token_type='Bearer')
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
