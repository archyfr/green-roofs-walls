import os
from dataclasses import dataclass, field
from typing import List
from pydantic import BaseModel


@dataclass(frozen=True)
class AppConfig:
    """Статическая конфигурация приложения, применяемая только при старте."""

    app_name: str = os.getenv("APP_NAME", "Оценка потенциала зеленых крыш")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    app_description: str = os.getenv("APP_DESCRIPTION", "Лабораторная работа по FastAPI")
    app_authors: List[str] = field(default_factory=lambda: ["Кондратенко Арина"])
    contact_email: str = os.getenv("CONTACT_EMAIL", "arinafr.99@gmail.com")

    def to_dict(self) -> dict:
        """Возвращает текущую статическую конфигурацию приложения."""
        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "app_description": self.app_description,
            "app_authors": self.app_authors,
            "contact_email": self.contact_email,
        }


class AppConfigResponse(BaseModel):
    app_name: str
    app_version: str
    app_description: str
    app_authors: List[str]
    contact_email: str


app_config = AppConfig()

