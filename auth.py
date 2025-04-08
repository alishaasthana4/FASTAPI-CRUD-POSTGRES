from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime,timedelta
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password:str):
    return pwd_context.hash(password)
def verify_password(plain_password,hashed_password)
    return pwd_context.verify(plain_password,hashed_password)
secret_key='defansh30e30e'
ALGORITHM='HS256'
access_token_expire_time=30 
def create_access_token(data:dict):
    to_encode=data.copy
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=access_token_expire_time)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt

    
    

