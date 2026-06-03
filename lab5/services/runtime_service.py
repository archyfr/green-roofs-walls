from typing import Optional
from pydantic import BaseModel


class RuntimeConfig(BaseModel):
    """Модель динамических параметров, которые можно изменять во время работы приложения."""

    log_level: str = "INFO"
    feature_flag: bool = False
    maintenance_mode: bool = False
    runtime_message: str = "Новый режим работы"


class RuntimeConfigService:
    """Сервис для хранения и обновления runtime-настроек в памяти приложения."""

    _instance: Optional["RuntimeConfigService"] = None
    _config: RuntimeConfig = RuntimeConfig()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get(self) -> RuntimeConfig:
        """Возвращает текущие runtime-настройки."""
        return self._config

    def update(self, data: dict) -> RuntimeConfig:
        """Обновляет runtime-настройки в памяти приложения."""
        updated = self._config.model_copy(update=data)
        self._config = updated
        return self._config


runtime_service = RuntimeConfigService()