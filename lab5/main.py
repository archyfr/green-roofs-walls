from fastapi import FastAPI
from config import app_config
from routes.health import router as health_router
from routes.config_routes import router as config_router

app = FastAPI(
    title=app_config.app_name,
    version=app_config.app_version,
    description=app_config.app_description,
)

app.include_router(health_router)
app.include_router(config_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)