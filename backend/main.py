from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import routers

app = FastAPI(
    title="METRIC",
    components={
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
    # Applies this scheme to all endpoints globally
    security=[{"BearerAuth": []}]
)

# 1. Define the list of origins that should be permitted to make requests.
origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]

# 2. Add the middleware to your app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Allows specific origins
    allow_credentials=True,      # Allows cookies/auth headers
    allow_methods=["*"],         # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],         # Allows all headers
)

Base.metadata.create_all(bind=engine)

app.include_router(routers.user)
app.include_router(routers.auth)
app.include_router(routers.chat)