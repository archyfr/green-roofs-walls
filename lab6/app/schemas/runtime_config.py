from typing import Literal
from pydantic import BaseModel, Field


class RuntimeConfigModel(BaseModel):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="INFO")
    feature_flag: bool = Field(default=False)
    maintenance_mode: bool = Field(default=False)
    runtime_message: str = Field(default="Приложение работает в штатном режиме")


class RuntimeConfigUpdateModel(BaseModel):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]
    feature_flag: bool
    maintenance_mode: bool
    runtime_message: str