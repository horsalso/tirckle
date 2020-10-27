from datetime import datetime, timedelta
import os
import uuid
from uuid import NAMESPACE_DNS
import jwt

class AppJwt:
    @staticmethod
    def Encode(username):
        dic = {
            'exp': datetime.now() + timedelta(days=1), 
            'iat': datetime.now(), 
            'iss': 'trickle', 
            'data': {  
                'username':username
                },
                }
        secrtKey=os.getenv('SECRET_KEY','SECRET_KEY')
        jwtStr=jwt.encode(dic,secrtKey,algorithm='HS256')
        return jwtStr
    @staticmethod
    def Decode(jwtStr):
        dic={}
        try:
            secrtKey=os.getenv('SECRET_KEY','SECRET_KEY')
            dic=jwt.decode(jwtStr,secrtKey,issur='trickle',algorithms=['HS256'])
        except:
            return None
        else:
            return dic

class AppResponse:
    @staticmethod
    def MakeResponse(status:str,message:str,data:dict={}):
        return {"status":status,"message":message,"data":data}

class UUIDBuilder:
    @staticmethod
    def UUID(seedName:str):
        uuid_32=str(uuid.uuid5(NAMESPACE_DNS,seedName)).replace('-','')
        return uuid_32

