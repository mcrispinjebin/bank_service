import logging
from fastapi import FastAPI, Request, status

from app import controller
from .config import env


env.initialize_env()

app = FastAPI(title="Bank Service",
              version="1.0.0",
              description="Bank service APIs documentation",
              docs_url="/bank_service/public/doc",
              redoc_url="/bank_service/public/redoc",
              openapi_url="/bank_service/public/openapi.json",
              openapi_tags=[])

app.include_router(controller.router, prefix="/bank_service/public/v1")


@app.get("/bank_service/public/ping", tags=['Health Check'])
async def ping():
    logging.info("ping request")
    return {"ping": "pong"}
