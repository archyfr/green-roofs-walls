from app.schemas.runtime_config import RuntimeConfigModel, RuntimeConfigUpdateModel


class RuntimeConfigService:
    def __init__(self, initial_config: RuntimeConfigModel):
        self._config = initial_config.model_copy(deep=True)

    def get_config(self) -> RuntimeConfigModel:
        return self._config

    def update_config(self, new_config: RuntimeConfigUpdateModel) -> RuntimeConfigModel:
        self._config = RuntimeConfigModel(**new_config.model_dump())
        return self._config