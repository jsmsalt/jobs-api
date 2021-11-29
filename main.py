import uuid
import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from settings import Settings
from logger import logger

from controllers.auth import router as auth_router
from controllers.permission import router as permission_router
from controllers.role import router as role_router
from controllers.session import router as session_router
from controllers.job import router as job_router
from controllers.user import router as user_router


app = FastAPI(
    title="Jobs Platform API",
    description="Simple jobs platform, using FastAPI (Starlette + Pydantic), \
        SQLModel (SQLAlchemy + Pydantic) and Alembic for migrations",
    version=Settings().version,
)

app.router.redirect_slashes = True


api_router = APIRouter(
    prefix='/api',
    redirect_slashes=False
)

api_router.include_router(auth_router)
api_router.include_router(job_router)
api_router.include_router(permission_router)
api_router.include_router(role_router)
api_router.include_router(session_router)
api_router.include_router(user_router)

app.include_router(api_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=['Content-Disposition']
)

# API Exception Handler


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    status_code = exc.status_code
    detail = str(exc.detail)

    if status_code == 500:
        exc_id = uuid.uuid4()
        logger.error(f"SERVER ERROR - ID={exc_id} , DETAIL={detail}")
        detail = f"An unexpected error occurred, please contact an \
            administrator with the following error code: {exc_id}"

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder({"detail": detail}),
    )


if __name__ == "__main__":
    uvicorn.run(app,
                host="0.0.0.0",
                port="80",
                log_level="warning",
                forwarded_allow_ips='*')
