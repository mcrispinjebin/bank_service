import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.core.custom_exception import BadRequest
from app import controller
from .config import env

tags_metadata = [
    {"name": "Account", "description": "Account Endpoints"},
    {"name": "Transaction", "description": "Transaction Endpoints"},
    {"name": "Health Check", "description": "Health check to verify service status"}
]

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


@app.exception_handler(Exception)
async def exception_handler(request: Request, error: Exception):
    """
    Handler method to override python exception
    :param request:
    :param error:
    :return:
    """
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=jsonable_encoder({"status": "failed", "message": "Internal server error"}))


@app.exception_handler(BadRequest)
async def bad_request_handler(request: Request, error: BadRequest):
    """
    Exception handler to handle 400 requests
    :param request:
    :param error:
    :return:
    """
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content=jsonable_encoder({"status": "failed", "message": error.message}))
