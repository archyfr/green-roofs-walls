import os
from pydantic import BaseModel, Field


class AppConfigModel(BaseModel):
    app_name: str = Field(default=os.getenv("APP_NAME", "Оценка потенциала зеленых крыш"))
    app_version: str = Field(default=os.getenv("APP_VERSION", "1.0.0"))
    app_description: str = Field(default=os.getenv("APP_DESCRIPTION", "Лабораторная работа по FastAPI"))
    app_authors: list[str] = Field(default=["Кондратенко Арина"])
    contact_email: str = Field(default=os.getenv("CONTACT_EMAIL", "arinafr.99@gmail.com"))