from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI(title="JWT FastAPI Example")

SECRET_KEY = "change-this-secret-in-production"
ALGORITHM = "HS256"
TOKEN_EXPIRE_SECONDS = 300
ADMIN_USERNAME = "admin"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
ADMIN_PASSWORD_HASH = pwd_context.hash("admin123")


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


def authenticate_user(username: str, password: str) -> bool:
    return username == ADMIN_USERNAME and pwd_context.verify(password, ADMIN_PASSWORD_HASH)


def create_access_token(username: str) -> str:
    expire_at = datetime.now(timezone.utc) + timedelta(seconds=TOKEN_EXPIRE_SECONDS)
    payload = {"sub": username, "exp": expire_at}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        return username
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc


@app.post("/token", response_model=TokenResponse)
def issue_token(credentials: LoginRequest) -> TokenResponse:
    if not authenticate_user(credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(credentials.username)
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=TOKEN_EXPIRE_SECONDS,
    )


@app.post("/token/refresh", response_model=TokenResponse)
def refresh_token(token: str = Depends(oauth2_scheme)) -> TokenResponse:
    username = decode_access_token(token)
    access_token = create_access_token(username)
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=TOKEN_EXPIRE_SECONDS,
    )
