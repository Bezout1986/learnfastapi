from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY="88ea08d7068874ed0551aedc75a35dcc6c44ae7f114377f7890383359f71eca6"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRES_MINUTES=30



db = {#db = { "shivanant":{  "username":"shiv",   "full_name": "Shiv Anant Tayal","email":"satayal@gmail.com",  "hashed_password":"$2b$12$W2IC0nwWXzKAIYarBeP7huO0wkq.2OtjM/GzJWHMv2RAyUn50L5t6",            "disabled":False  } }
        "tim":{
            "username":"tim",
            "full_name": "John Doe",
            "email":"tim@gmail.com",
            "hashed_password":"$2b$12$W2IC0nwWXzKAIYarBeP7huO0wkq.2OtjM/GzJWHMv2RAyUn50L5t6",
            "disabled":False

            }
        }


class Token(BaseModel):
    access_token: str
    token_type:str

class TokenData(BaseModel):
    username:str or None=None
    
class User(BaseModel):
    username:str
    email:str or None=None
    full_name:str or None=None
    disabled: bool or None=None
    
class UserinDB(User):
    hashed_password:str


pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        return UserinDB(**user_data)

def authenticate_user(db, username: str, password:str):
    user=get_user(db,username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user

def create_access_token(data:dict, expires_delta: timedelta or None=None):
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.utcnow() + expires_delta
    else:
        expire=datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    print(oauth2_scheme)
    print(token)
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    try: 
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data= TokenData(username=username)


    except JWTError:
        raise credential_exception

    user=get_user(db,username=token_data.username)
    if user is None:
        raise credential_exception
    return user


async def get_current_active_user(current_user:UserinDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="inactive user")
    return current_user

app=FastAPI()

@app.post("/token",response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user=authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="incorrect username or password", headers= {"WWW-Authenticate":"Bearer"})

    access_token_expires = timedelta (minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token=create_access_token(data={"sub":user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type":"bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user :User=Depends(get_current_active_user)):
    return current_user

@app.get("/user/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id":1, "owner": current_user}]

