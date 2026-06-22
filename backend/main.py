from fastapi import FastAPI, routing
from database import engine, Base
import routers

app = FastAPI(
    title="Role-Based Access Mock",
    description="Simulating JWT roles using integers."
)

Base.metadata.create_all(bind=engine)

app.include_router(routers.user)
app.include_router(routers.auth)