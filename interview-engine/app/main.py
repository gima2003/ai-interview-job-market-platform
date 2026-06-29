from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Interview Intelligence Engine")
app.include_router(router)
