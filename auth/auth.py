import jwt
from datetime import datetime, timedelta
from typing import Union, Any

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import ValidationError


class AuthHandler:
    SECURITY_ALGORITHM = 'HS256'
    SECRET_KEY = 'SECRET_KEY'

    reusable_oauth2 = HTTPBearer(scheme_name='Authorization')

    def generate_token(self, username: Union[str, Any]) -> str:
        expire = datetime.utcnow() + timedelta(seconds=60 * 60 * 24 * 3)
        to_encode = {
            "exp": expire,
            "username": username
        }
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.SECURITY_ALGORITHM)
        return encoded_jwt

    def validate_token(self, http_authorization_credentials=Depends(reusable_oauth2)) -> str:
        try:
            payload = jwt.decode(http_authorization_credentials.credentials, self.SECRET_KEY,
                                 algorithms=[self.SECURITY_ALGORITHM])
            if payload.get('username') < str(datetime.now()):
                raise HTTPException(status_code=403, detail="Token expired")
            return payload.get('username')
        except(jwt.PyJWTError, ValidationError):
            raise HTTPException(status_code=403, detail="Could not validate credentials")
