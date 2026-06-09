from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TerritoryBase(BaseModel):
    """Базовые поля территории."""

    name: str
    territory_type: str
    level: int = Field(ge=0)
    description: str | None = None
    geom_wkt: str


class TerritoryCreate(TerritoryBase):
    """Схема для создания территории."""
    pass


class TerritoryUpdate(BaseModel):
    """Схема для обновления территории — все поля необязательные."""

    name: str | None = None
    territory_type: str | None = None
    level: int | None = Field(default=None, ge=0)
    description: str | None = None
    geom_wkt: str | None = None


class TerritoryRead(BaseModel):
    """Схема для чтения территории."""

    id: int
    name: str
    territory_type: str
    level: int
    description: str | None
    geom_wkt: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TerritoryMetricCreate(BaseModel):
    """Схема для создания показателя территории."""

    year: int
    population: int | None = None
    area_km2: Decimal | None = None
    source: str | None = None


class TerritoryMetricUpdate(BaseModel):
    """Схема для обновления показателя территории — все поля необязательные."""

    year: int | None = None
    population: int | None = None
    area_km2: Decimal | None = None
    source: str | None = None


class TerritoryMetricRead(BaseModel):
    """Схема для чтения показателя территории."""

    id: int
    territory_id: int
    year: int
    population: int | None
    area_km2: Decimal | None
    source: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
