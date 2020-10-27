from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class UserBase(BaseModel):
    name:str
    passwords:str
    
class UserRegister(BaseModel):
    nickname:str
    email:str=None
    passwords_comform:str
    registertime:datetime=None
    lastlogin:datetime=None

class Auth(str,Enum):
    signin='signin'
    signup='signup'
    