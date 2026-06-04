"""Загрузка и первичная валидация геоданных зданий."""

from pathlib import Path
from typing import Union

import geopandas as gpd
from green_potential.exceptions import EmptyDataError, InvalidGeometryError
from loguru import logger


def load_buildings(path: Union[str, Path]) -> gpd.GeoDataFrame:
    """Загрузка геоданных зданий и фильтрация невалидной геометрии.

    Args:
        path: Путь до файла с геоданными (.gpkg, .shp и др.).

    Returns:
        GeoDataFrame с непустыми и валидными геометриями.

    Raises:
        FileNotFoundError: Если файл не найден по указанному пути.
        InvalidGeometryError: Если данные не содержат столбец geometry.
        EmptyDataError: Если после фильтрации не осталось ни одного здания.
        RuntimeError: При любой другой ошибке чтения файла.
    """
    path = Path(path)
    logger.info("Загрузка геоданных из: {}", path)

    try:
        gdf = gpd.read_file(path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл не найден: {path}") from e
    except Exception as e:
        raise RuntimeError(f"Не удалось прочитать файл: {path}") from e

    if "geometry" not in gdf.columns:
        raise InvalidGeometryError("Данные не содержат столбец 'geometry'")

    before = len(gdf)
    gdf = gdf[gdf.geometry.notna() & gdf.geometry.is_valid]
    dropped = before - len(gdf)

    if dropped:
        logger.warning(
            "Отфильтровано {} зданий с пустой или невалидной геометрией", dropped
        )

    if gdf.empty:
        raise EmptyDataError("После фильтрации геометрии не осталось ни одного здания")

    logger.info("Загружено {} зданий", len(gdf))
    return gdf
