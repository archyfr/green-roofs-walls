from fastapi import APIRouter
from config import app_config, AppConfigResponse
from services.runtime_service import RuntimeConfig, runtime_service

router = APIRouter(prefix="/config", tags=["Configuration"])


@router.get(
    "/app",
    response_model=AppConfigResponse,
    summary="Получение статической конфигурации",
    description="Возвращает текущую статическую конфигурацию приложения."
)
def get_app_config():
    """Возвращает текущую статическую конфигурацию приложения."""
    return app_config.to_dict()


@router.get(
    "/runtime",
    response_model=RuntimeConfig,
    summary="Получение динамических параметров",
    description="Возвращает текущие runtime-настройки."
)
def get_runtime_config():
    """Возвращает текущие runtime-настройки."""
    return runtime_service.get()


@router.put(
    "/runtime",
    response_model=RuntimeConfig,
    summary="Обновление динамических параметров",
    description="Принимает JSON с новыми значениями динамических параметров и обновляет их в памяти приложения."
)
def update_runtime_config(updates: RuntimeConfig):
    """Принимает JSON с новыми значениями динамических параметров и обновляет их в памяти приложения."""
    updated = runtime_service.update(updates.model_dump())
    return updated