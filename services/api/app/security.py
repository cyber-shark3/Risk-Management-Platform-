"""Password hashing and short-lived JWT access tokens."""
from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from .config import settings

_password_hash = PasswordHash.recommended()
_ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return _password_hash.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return _password_hash.verify(password, password_hash)
    except Exception:
        return False


def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {"sub": str(user_id), "iat": now, "exp": now + timedelta(minutes=settings.access_token_minutes)},
        settings.secret_key,
        algorithm=_ALGORITHM,
    )


def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, settings.secret_key, algorithms=[_ALGORITHM])
    subject = payload.get("sub")
    if not subject or not str(subject).isdigit():
        raise jwt.InvalidTokenError("Invalid subject")
    return int(subject)
