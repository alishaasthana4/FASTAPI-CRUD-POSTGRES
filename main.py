from fastapi import FastAPI,Depends,HTTPException,status,Header
from models import DBUser
from database import engine,Base
from schemas import Userr,LoginInput,ChangePassword
from database import sessionlocal
from auth import hash_password,verify_password,create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import generate_api_key
def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()
app=FastAPI()
Base.metadata.create_all(engine)
def get_by_api_key(api_key:str=Header(...),db: Session=Depends(get_db)):
    user=db.query(DBUser).filter(DBUser.api_key==api_key).first()
    if not user:
        raise HTTPException(status_code=400,detail="API Key not valid")
    return user
@app.post("/login")
def login(user:LoginInput,db: Session=Depends(get_db)):
    db_user=db.query(DBUser).filter(DBUser.email==user.email).first()
    if not db_user or not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=400,detail="Invalid Credentials")
    token = create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}
@app.post("/signup", status_code=201)
def signup(user: Userr, db: Session = Depends(get_db)):
    existing_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User with this email already exists")
    hashed_pw = hash_password(user.password)
    api_key=generate_api_key()
    new_user = DBUser(name=user.name, email=user.email, password=hashed_pw, api_key=api_key)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message": "User created successfully",
        "user": {
            "name": new_user.name,
            "email": new_user.email,
            "api_key":api_key
        }
    }
@app.post("/ChangePassword",status_code=201)
def change_password(user:ChangePassword,db:Session=Depends(get_db),current_user: DBUser = Depends(get_by_api_key)):
    db_user=db.query(DBUser).filter(DBUser.email==user.email).first()
    if not db_user:
        raise HTTPException(status_code=404,detail="User Not Found")
    if not verify_password(user.old_password,db_user.password):
        raise HTTPException(status=404,detail="Old Password is incorrect")
    db_user.password=hash_password(user.new_password)
    db.commit()
    return{"message":"Password changes Successfully"}
@app.post("/users")
def create_users(user:Userr,db:Session=Depends(get_db),current_user: DBUser = Depends(get_by_api_key)):
    hash_pw=hash_password(user.password)
    api_key=generate_api_key()
    db_user=DBUser(name=user.name,email=user.email,password=hash_pw,api_key=api_key)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
@app.get("/users")
def get_users(db:Session=Depends(get_db),current_user: DBUser = Depends(get_by_api_key)):
    return db.query(DBUser).all()
@app.put("/users/{user_id}")
def update_users(user_id:int,user:Userr,db:Session=Depends(get_db),current_user: DBUser = Depends(get_by_api_key)):
    db_user=db.query(DBUser).get(user_id)
    if not db_user:
        return{"Error":"User_id not found"}
    db_user.name=user.name
    db_user.email=user.email
    db.commit()
    db.refresh(db_user)
    return(db_user)
@app.delete("/users")
def delete_user(user_id:int,db:Session=Depends(get_db),current_user: DBUser = Depends(get_by_api_key)):
    db_user=db.query(DBUser).get(user_id)
    if not db_user:
        return {"error": "User not found. Nothing to delete "}
    db.delete(db_user)
    db.commit()
    return {"message": f"User with ID {user_id} has been deleted "}
    

    
    
    	
    
    
    


    
    

                       

   



    







