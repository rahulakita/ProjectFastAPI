from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Merchant
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
SECRET_KEY = '0812syafrinal6776669'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateMerchantRequest(BaseModel):
    username : str
    plainpassword : str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


@router.post("/merchant/daftar/", status_code=status.HTTP_201_CREATED)
async def create_merch(Merchant_req: CreateMerchantRequest, db: db_dependency):
    buatmerchant= Merchant(
        usermerchant=Merchant_req.username,
        password=bcrypt_context.hash(Merchant_req.plainpassword)
    )
    db.add(buatmerchant)
    db.commit()
    return JSONResponse(content={"status":buatmerchant.password})

@router.post("/token", response_model=Token)
async def login_for_access_token (form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = autentifikasi_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Merchant tidak terdaftar')
    token = create_access_token(user.usermerchant, user.idm, timedelta(minutes=30))
    return {'access_token': token, 'token_type': 'bearer'}

def autentifikasi_user(authusername: str, authpassword: str, db):
    user = db.query(Merchant).filter(Merchant.usermerchant == authusername).first()
    if not user:
        return False
    if not verify_password(authpassword, user.password):
        return False
    return user
def create_access_token(user_name: str, user_id:int, expires_delta: timedelta):
    encode = {'sub': user_name, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Merchant tidak tervalidasi')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Merchant tidak tervalidasi')
    