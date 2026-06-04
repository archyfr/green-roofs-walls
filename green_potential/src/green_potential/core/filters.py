"""Фильтрация зданий по атрибутам: тип крыши, год постройки."""

import geopandas as gpd
from green_potential.exceptions import (
    EmptyDataError,
    InvalidYearError,
    MissingColumnError,
)
from loguru import logger

# Типы крыш, потенциально пригодных для озеленения
GREENABLE_ROOF_TYPES: set[str] = {"flat", "shed"}


def filter_by_roof_type(
    gdf: gpd.GeoDataFrame,
    roof_type: str,
    roof_column: str = "roof:shape",
) -> gpd.GeoDataFrame:
    """Фильтрация зданий по типу крыши.

    Args:
        gdf: Таблица зданий.
        roof_type: Тип крыши для фильтрации (например, "flat", "gabled").
        roof_column: Имя столбца с типом крыши.

    Returns:
        GeoDataFrame только со зданиями указанного типа крыши.

    Raises:
        MissingColumnError: Если столбец roof_column отсутствует в данных.
        EmptyDataError: Если зданий с указанным типом крыши не найдено.
    """
    if roof_column not in gdf.columns:
        raise MissingColumnError(
            f"В данных нет столбца '{roof_column}' для фильтрации по типу крыши"
        )

    result = gdf[gdf[roof_column] == roof_type]

    if result.empty:
        raise EmptyDataError(
            f"Нет зданий с типом крыши '{roof_type}' в столбце '{roof_column}'"
        )

    logger.info("Найдено {} зданий с типом крыши '{}'", len(result), roof_type)
    return result


def filter_greenable_roofs(
    gdf: gpd.GeoDataFrame,
    roof_column: str = "roof:shape",
) -> gpd.GeoDataFrame:
    """Фильтрация зданий с крышами, пригодными для озеленения (flat, shed).

    Плоские и односкатные крыши считаются наиболее подходящими для
    размещения зелёных кровель в холодном климате.

    Args:
        gdf: Таблица зданий.
        roof_column: Имя столбца с типом крыши.

    Returns:
        GeoDataFrame с потенциально озеленяемыми зданиями.

    Raises:
        MissingColumnError: Если столбец roof_column отсутствует в данных.
        EmptyDataError: Если подходящих зданий не найдено.
    """
    if roof_column not in gdf.columns:
        raise MissingColumnError(f"В данных нет столбца '{roof_column}'")

    result = gdf[gdf[roof_column].isin(GREENABLE_ROOF_TYPES)]

    if result.empty:
        raise EmptyDataError("Не найдено зданий с крышами, пригодными для озеленения")

    logger.info(
        "Найдено {} зданий с пригодными для озеленения крышами (из {})",
        len(result),
        len(gdf),
    )
    return result


def sort_by_year(
    gdf: gpd.GeoDataFrame,
    year_column: str = "start_date",
    ascending: bool = True,
) -> gpd.GeoDataFrame:
    """Сортировка зданий по году постройки.

    Args:
        gdf: Таблица зданий.
        year_column: Имя столбца с годом постройки.
        ascending: Порядок сортировки (True — от старых к новым).

    Returns:
        Отсортированный GeoDataFrame.

    Raises:
        MissingColumnError: Если столбец year_column отсутствует в данных.
        InvalidYearError: Если столбец содержит нечисловые значения.
    """
    if year_column not in gdf.columns:
        raise MissingColumnError(
            f"В данных нет столбца '{year_column}' для сортировки по году"
        )

    non_numeric = (
        gdf[year_column].dropna().map(lambda v: not isinstance(v, (int, float)))
    )
    if non_numeric.any():
        raise InvalidYearError(
            f"Столбец '{year_column}' должен содержать числовые значения (год постройки)"
        )

    return gdf.sort_values(year_column, ascending=ascending)


def buildings_without_year(
    gdf: gpd.GeoDataFrame,
    year_column: str = "start_date",
) -> gpd.GeoDataFrame:
    """Выборка зданий без информации о годе постройки.

    Args:
        gdf: Таблица зданий.
        year_column: Имя столбца с годом постройки.

    Returns:
        GeoDataFrame только с записями, где год постройки отсутствует.

    Raises:
        MissingColumnError: Если столбец year_column отсутствует в данных.
    """
    if year_column not in gdf.columns:
        raise MissingColumnError(f"В данных нет столбца '{year_column}'")

    result = gdf[gdf[year_column].isna()]
    logger.info("Зданий без года постройки: {}", len(result))
    return result
