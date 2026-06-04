from app.schemas.app_config import AppConfigModel
from app.schemas.runtime_config import RuntimeConfigModel
from app.services.runtime_config_service import RuntimeConfigService


class DependencyContainer(dict):
    def get_required(self, key: str):
        if key not in self:
            raise KeyError(f"Dependency '{key}' is not initialized")
        return self[key]


dependencies_container = DependencyContainer()


def init_dependencies() -> DependencyContainer:
    app_config = AppConfigModel()
    runtime_config = RuntimeConfigModel()
    runtime_service = RuntimeConfigService(initial_config=runtime_config)

    dependencies_container["app_config"] = app_config
    dependencies_container["runtime_config_service"] = runtime_service

    return dependencies_container