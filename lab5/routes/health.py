from fastapi import APIRouter
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


router = APIRouter()

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Проверка работоспособности приложения",
    description="Возвращает информацию о том, что приложение запущено."
)
def health_check():
    """Возвращает информацию о том, что приложение запущено."""
    return {"status": "ok"}