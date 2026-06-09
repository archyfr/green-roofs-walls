from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.territories.router import router as territories_router

app = FastAPI(
    title="Urban Spatial Database API",
    description="CRUD-сервис для городских территорий и показателей.",
    version="1.0.0",
)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get(
    "/health",
    summary="Проверка работоспособности приложения",
    description="Возвращает информацию о том, что приложение запущено.",
)
def health_check():
    """Возвращает информацию о том, что приложение запущено."""
    return {"status": "ok"}


app.include_router(territories_router)
