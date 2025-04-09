from passlib.context import CryptContext
import jwt
from datetime import datetime,timedelta,timezone
pwd_context=CryptContext(schemes='bcrypt',deprecated='auto')
def hash_password(password:str):
    return pwd_context.hash(password)
def verify_password(hashed_password,plain_password):
    return pwd_context.verify(hashed_password,plain_password)
Secret_key='ali29330eie0'
ALGORITHM='HS256'
access_token_time=30
def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc) + timedelta(minutes=access_token_time)
    to_encode.update({'exp':expire})
    encoded_jwt=jwt.encode(to_encode,Secret_key,algorithm=ALGORITHM)
    return encoded_jwt
    


    
                               
    

