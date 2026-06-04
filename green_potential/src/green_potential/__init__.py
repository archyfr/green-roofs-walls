"""green_potential — библиотека оценки потенциала озеленения зданий.

Анализ зданий на пригодность размещения зелёных крыш
и вертикальных систем озеленения с учётом пространственных данных."""

from green_potential.core.filters import (
    buildings_without_year,
    filter_by_roof_type,
    filter_greenable_roofs,
    sort_by_year,
)
from green_potential.core.loader import load_buildings
from green_potential.exceptions import (
    EmptyDataError,
    GreenPotentialError,
    InvalidGeometryError,
    InvalidRoofTypeError,
    InvalidYearError,
    MissingColumnError,
)
from green_potential.services.potential import BuildingScorer
from green_potential.services.spatial import coverage_ratio, top_districts
from green_potential.utils.crs import assert_same_crs, ensure_metric_crs

__all__ = [
    # Загрузка данных
    "load_buildings",
    # Фильтрация
    "filter_by_roof_type",
    "filter_greenable_roofs",
    "sort_by_year",
    "buildings_without_year",
    # Оценка потенциала
    "BuildingScorer",
    # Пространственный анализ
    "coverage_ratio",
    "top_districts",
    # Утилиты CRS
    "ensure_metric_crs",
    "assert_same_crs",
    # Исключения
    "GreenPotentialError",
    "EmptyDataError",
    "InvalidGeometryError",
    "MissingColumnError",
    "InvalidRoofTypeError",
    "InvalidYearError",
]
