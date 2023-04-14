from fastapi import APIRouter, HTTPException, status

from ..schemas import JWTToken, SignIn, SignUp
from ..services import auth_service, user_service

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/signin")
async def signin(sigin_schema: SignIn):
    authenticated = await auth_service.authenticate(
        sigin_schema.username, sigin_schema.password
    )
    if authenticated:
        access_token = auth_service.create_access_token(
            data={"sub": authenticated.username}
        )
        return JWTToken(token=access_token, token_type="bearer")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/signup")
async def signup(signup_schema: SignUp):
    user = await user_service.get(
        username=signup_schema.username,
        email=signup_schema.email,
        mobile=signup_schema.mobile,
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or email or mobile",
            headers={"WWW-Authenticate": "Bearer"},
        )
    await user_service.create(
        username=signup_schema.username,
        mobile=signup_schema.mobile,
        password=signup_schema.password1,
        email=signup_schema.email,
    )
    return {"status": "success"}
