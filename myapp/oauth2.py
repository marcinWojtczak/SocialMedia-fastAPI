from jose import JWTError, jwt
from datetime import datetime, timedelta
from myapp import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from myapp.config import settings


# This parameter contains the URL that the client (the frontend running in the user's browser)
# will use to send the username and password in order to get a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


# Token structure:
# Header (algorithm, token type)
# Payload
# Signature (Header+Payload+Secret)+ hashing func


def create_access_token(data: dict):  # data -> payload
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # payload, secret, header
    # to_encode -> everything we want to put in to payload in our case wy add token expire
    return encoded_jwt


# check if password received from users is equal hashed password in db
def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # extract date from payload
        id: str = payload.get("user_email")
        if id is None:
            raise credentials_exceptions
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exceptions

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.email == token.id).first()
    return user
