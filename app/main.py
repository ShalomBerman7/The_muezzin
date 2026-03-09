from fastapi import FastAPI
from routes import route


app = FastAPI()

app.include_router(route)


