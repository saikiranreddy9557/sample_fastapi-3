from datetime import datetime, timedelta

import uvicorn


from fastapi import Depends, FastAPI, HTTPException, status,Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from auth_utils import verify_password,get_password_hash,get_user,authenticate_user,create_access_token,get_current_user,get_current_active_user,get_current_user_entities

from test_user_data import fake_users_db

from models_test import Token,TokenData,User,UserInDB,Entities
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI()







@app.post("/login/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username,"company":user.company}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer","is_super_user":user.super_user}


@app.get("/entities/",response_model=Entities)
async def read_users_me(current_user: User = Depends(get_current_user_entities)):
    
    return {"entity_list":current_user}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]



