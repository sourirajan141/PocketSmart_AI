from datetime import datetime, timedelta, timezone
import base64, hashlib, hmac, os
import jwt
from .config import settings

ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    salt=os.urandom(16)
    digest=hashlib.pbkdf2_hmac("sha256",password.encode(),salt,210000)
    return "pbkdf2_sha256$210000$"+base64.urlsafe_b64encode(salt).decode()+"$"+base64.urlsafe_b64encode(digest).decode()

def verify_password(password: str, stored: str) -> bool:
    try:
        scheme,iters,salt_b64,digest_b64=stored.split("$")
        salt=base64.urlsafe_b64decode(salt_b64.encode())
        expected=base64.urlsafe_b64decode(digest_b64.encode())
        actual=hashlib.pbkdf2_hmac("sha256",password.encode(),salt,int(iters))
        return hmac.compare_digest(actual,expected)
    except Exception:
        return False

def create_access_token(user_id: int) -> str:
    expire=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub":str(user_id),"exp":expire},settings.secret_key,algorithm=ALGORITHM)

def decode_access_token(token: str) -> int:
    payload=jwt.decode(token,settings.secret_key,algorithms=[ALGORITHM])
    return int(payload["sub"])
