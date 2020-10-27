from fastapi import APIRouter,UploadFile,File
from typing import List
import os
from ext.exts import AppResponse
base=APIRouter()

@base.post('/photos')
async def PhotoUpload(files:List[UploadFile]=File(...)):
    filenames=[]
    for file in files:
        contents=await file.read()
        filenames.append(file.filename)
        storePath=os.getenv('IMAGE_STORE_PATH','')
        with open(storePath+file.filename+'.jpg','wb') as im:
            im.write(contents)
    return AppResponse.MakeResponse('200','上传成功',{'文件名称':filenames})