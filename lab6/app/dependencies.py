from app.init_dependencies import dependencies_container
from app.schemas.app_config import AppConfigModel
from app.services.runtime_config_service import RuntimeConfigService


def get_app_config() -> AppConfigModel:
    return dependencies_container.get_required("app_config")


def get_runtime_config_service() -> RuntimeConfigService:
    return dependencies_container.get_required("runtime_config_service")