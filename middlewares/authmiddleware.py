import json
import typing
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from starlette.datastructures import Headers
from starlette.responses import Response
from ext.exts import AppResponse,AppJwt

class authmiddleware:
    def __init__(self,app:ASGIApp,except_domain:str):
        self.app=app
        self.except_domain=except_domain

    async def __call__(self,scope:Scope,receive:Receive,send:Send)->None:
        if scope['type'] !='http':
            await self.app(scope,receive,send)
            return
        headers=Headers(scope=scope)
        path=scope['path']
        excepts=self.UnpackDomain(self.except_domain)
        if path in excepts:
            await self.app(scope,receive,send)
            return
        jwtStr=headers.get('Authorization')
        if jwtStr==None:
            await Response(content=json.dumps(AppResponse.MakeResponse('401','鉴权失败'),ensure_ascii=False),status_code=401)(scope,receive,send)      
            return
        else:
            print(jwtStr)
            jwtDic=self.JWTAuthority(jwtStr)
            if jwtDic==None:
                await Response(content=json.dumps(AppResponse.MakeResponse('401','鉴权失败'),ensure_ascii=False),status_code=401)(scope,receive,send)      
                return
            else:
                await self.app(scope,receive,send)
                return

    def UnpackDomain(self,domainStr:str)->typing.Sequence[str]:
        return domainStr.split(';')
    
    def JWTAuthority(self,jwtStr:str)->dict:
        jwtStr=jwtStr[7:]
        authRes=AppJwt.Decode(jwtStr)
        return authRes

    