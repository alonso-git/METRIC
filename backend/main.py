from fastapi import FastAPI, routing
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

Base.metadata.create_all(bind=engine)

app.include_router(routers.user)
app.include_router(routers.auth)