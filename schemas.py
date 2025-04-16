from pydantic import BaseModel
class Userr(BaseModel):
    name: str
    email: str
    id: int
    password:str
class LoginInput(BaseModel):
    email:str
    password:str
class ChangePassword(BaseModel):
    old_password:str
    new_password:str
    email:str
    
    






