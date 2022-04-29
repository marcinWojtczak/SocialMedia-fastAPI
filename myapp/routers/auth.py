from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from my_api.myapp import database, models, schemas, utils, oauth2


router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # OAuth2 specifies that client/user must send a username, you can show it as you wish to your final
    # users in the frontend
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    # check if password that user provide is == password form db
    if not utils.verify_password(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    # user_id is data that we want to put in payload
    access_token = oauth2.create_access_token(data={"user_email": user.email})

    return {"access_token": access_token, "token_type": "bearer"}




