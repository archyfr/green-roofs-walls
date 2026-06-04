from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.dependencies import get_app_config
from app.init_dependencies import init_dependencies
from app.routes.config import router as config_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_dependencies()
    yield


init_dependencies()
app_config = get_app_config()

app = FastAPI(
    lifespan=lifespan,
    title=app_config.app_name,
    description=app_config.app_description,
    version=app_config.app_version,
)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/ping", include_in_schema=False)
async def ping():
    return "pong"


app.include_router(config_router)