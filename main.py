from fastapi import FastAPI,Depends,HTTPException,status
from models import DBUser
from database import engine,Base,Session
from schemas import Userr
from database import sessionlocal
def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()
app=FastAPI()
Base.metadata.create_all(engine)
@app.post("/users")
def create_users(user:Userr,db:Session=Depends(get_db)):
    db_user=DBUser(id=user.id,name=user.name,email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
@app.get("/users")
def get_users(db:Session=Depends(get_db)):
    return db.query(DBUser).all()
@app.put("/users/{user_id}")
def update_users(user_id:int,user:Userr,db:Session=Depends(get_db)):
    db_user=db.query(DBUser).get(user_id)
    if not db_user:
        return{"Error":"User_id not found"}
    db_user.id=user.id
    db_user.name=user.name
    db_user.email=user.email
    db.commit()
    db.refresh(db_user)
    return(db_user)
@app.delete("/users")
def delete_user(user_id:int,db:Session=Depends(get_db)):
    db_user=db.query(DBUser).get(user_id)
    if not db_user:
        return {"error": "User not found. Nothing to delete "}
    db.delete(db_user)
    db.commit()
    return {"message": f"User with ID {user_id} has been deleted "}

   



    







