from fastapi import FastAPI
from routes import book_routes


app = FastAPI()


app.include_router(book_routes.router)