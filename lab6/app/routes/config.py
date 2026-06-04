from fastapi import APIRouter, Depends

from app.dependencies import get_app_config, get_runtime_config_service
from app.schemas.app_config import AppConfigModel
from app.schemas.responses import HealthResponse
from app.schemas.runtime_config import RuntimeConfigModel, RuntimeConfigUpdateModel
from app.services.runtime_config_service import RuntimeConfigService

router = APIRouter(tags=["configuration"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Проверка работоспособности приложения",
    description="Возвращает информацию о том, что приложение запущено."
)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get(
    "/config/app",
    response_model=AppConfigModel,
    summary="Получение статической конфигурации",
    description="Возвращает текущую статическую конфигурацию приложения."
)
def get_app_configuration(
    app_config: AppConfigModel = Depends(get_app_config),
) -> AppConfigModel:
    return app_config


@router.get(
    "/config/runtime",
    response_model=RuntimeConfigModel,
    summary="Получение runtime-конфигурации",
    description="Возвращает текущие runtime-настройки."
)
def get_runtime_configuration(
    runtime_service: RuntimeConfigService = Depends(get_runtime_config_service),
) -> RuntimeConfigModel:
    return runtime_service.get_config()


@router.put(
    "/config/runtime",
    response_model=RuntimeConfigModel,
    summary="Обновление runtime-конфигурации",
    description="Принимает JSON с новыми значениями динамических параметров и обновляет их в памяти приложения."
)
def update_runtime_configuration(
    updates: RuntimeConfigUpdateModel,
    runtime_service: RuntimeConfigService = Depends(get_runtime_config_service),
) -> RuntimeConfigModel:
    return runtime_service.update_config(updates)