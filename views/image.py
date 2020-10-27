from fastapi import APIRouter,UploadFile,File

base=APIRouter()

base.post('/photos')
async def PhotoUpload(file:UploadFile=File(...)):
    contents=await file.read()
