"""Утилиты для работы с системами координат (CRS)."""

import geopandas as gpd
from green_potential.exceptions import EmptyDataError
from loguru import logger

# EPSG для метрической проекции России (UTM zone 36N)
DEFAULT_METRIC_CRS = 32636


def ensure_metric_crs(
    gdf: gpd.GeoDataFrame,
    target_epsg: int = DEFAULT_METRIC_CRS,
) -> gpd.GeoDataFrame:
    """Привести GeoDataFrame к метрической проекции.

    Если CRS уже метрическая — данные не изменяются.
    Если CRS географическая (градусы) — перепроецируется в target_epsg.

    Args:
        gdf: Исходный GeoDataFrame.
        target_epsg: EPSG-код целевой метрической проекции.

    Returns:
        GeoDataFrame в метрической проекции.

    Raises:
        EmptyDataError: Если GeoDataFrame пуст.

    Example:
        >>> buildings_m = ensure_metric_crs(buildings)
        >>> buildings_m.crs.to_epsg()
        32636
    """
    if gdf.empty:
        raise EmptyDataError("Передан пустой GeoDataFrame")

    if gdf.crs is None:
        logger.warning("CRS не задан, устанавливаем EPSG:4326 и перепроецируем")
        gdf = gdf.set_crs(4326)

    if gdf.crs.is_geographic:
        logger.info("Перепроецируем из {} → EPSG:{}", gdf.crs, target_epsg)
        return gdf.to_crs(target_epsg)

    return gdf


def assert_same_crs(
    gdf1: gpd.GeoDataFrame,
    gdf2: gpd.GeoDataFrame,
) -> None:
    """Проверить совпадение CRS двух GeoDataFrame.

    Args:
        gdf1: Первый GeoDataFrame.
        gdf2: Второй GeoDataFrame.

    Raises:
        ValueError: Если CRS не совпадают.

    Example:
        >>> assert_same_crs(buildings, districts)  # не вызывает ошибку
    """
    if gdf1.crs != gdf2.crs:
        raise ValueError(
            f"CRS не совпадают: {gdf1.crs} vs {gdf2.crs}. "
            "Используйте ensure_metric_crs() для приведения к единой проекции."
        )
