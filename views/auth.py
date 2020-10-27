import datetime
import os
import uuid
from uuid import NAMESPACE_DNS
from fastapi import APIRouter,Depends
import jwt
from schmas.user import Auth,UserRegister,UserBase
from database import SessionLocal,BaseDBMode,engine
from sqlalchemy.orm import Session
from models import Album, Photo, User
from werkzeug.security import generate_password_hash,check_password_hash
from ext.exts import AppJwt,AppResponse,UUIDBuilder

router=APIRouter()

def get_db():
    db = ''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.post('/users')
async def UserAuth(auth:Auth,signin:UserBase,signup:UserRegister=None,db:Session=Depends(get_db)):
    if auth==Auth.signin:
        return UserSigninAuth(db,signin)
    elif auth==Auth.signup:
        return UserSignupAuth(db,signin,signup)

def UserSigninAuth(db:Session,signinInfo:UserRegister):
    curUser=db.query(User).filter(User.name==signinInfo.name).first()
    if curUser==None:
        return AppResponse.MakeResponse('404','用户不存在',)
    userExist=check_password_hash(curUser.passwords,signinInfo.passwords)
    if userExist:       
        jwtStr=AppJwt.Encode(signinInfo.name)
        curUser.lastlogin=datetime.datetime.now()
        db.commit()
        return AppResponse.MakeResponse('200','登陆成功',{'token':jwtStr})
    return AppResponse.MakeResponse('404','密码错误')

def UserSignupAuth(db:Session,signinInfo:UserBase,signupInfo:UserRegister):
    if db.query(User).filter(User.name==signinInfo.name).first():
        return AppResponse.MakeResponse('404','用户已存在')
    if signinInfo.passwords!=signupInfo.passwords_comform:
        return AppResponse.MakeResponse('404','两次密码不一致')
    passwords=generate_password_hash(signinInfo.passwords)
    userUUID=UUIDBuilder.UUID(signinInfo.name)
    newUser=User(uid=userUUID,name=signinInfo.name,passwords=passwords,nickname=signupInfo.nickname,email=signupInfo.email,lastlogin=datetime.datetime.now())
    
    db.add(newUser)
    db.commit()
    db.refresh(newUser)   
    jwtStr=AppJwt.Encode(signinInfo.name)
    return  AppResponse.MakeResponse('200','注册成功',{'token':jwtStr})

@router.get('/DataBase')
def DataBaseOperation(method:str):
    if method=='init':
        print(method)
        BaseDBMode.metadata.create_all(engine)
        return AppResponse.MakeResponse('200','数据库创建成功')
    elif method=='drop':
        BaseDBMode.metadata.drop_all(engine)
        return AppResponse.MakeResponse('200','数据库清除成功')

@router.get('/test')
async def testAuthMiddleware():
    return AppResponse.MakeResponse('200','测试请求')