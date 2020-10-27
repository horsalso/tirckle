import os
from dotenv import load_dotenv
def env_load():
    load_dotenv(verbose=True)
env_load()  
from middlewares.authmiddleware import authmiddleware
from fastapi import FastAPI
import views.auth

def create_app():
    app=FastAPI()
    ##app.add_middleware(authmiddleware,except_domain=os.getenv('AUTHMIDDLE_EXCEPT_DOMAIN',''))
    app.include_router(views.auth.router,prefix='/api')
    return app
  
app=create_app()

