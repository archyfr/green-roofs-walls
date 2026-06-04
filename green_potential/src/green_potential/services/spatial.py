"""Пространственный анализ: буферы, покрытие, агрегация по районам."""

import geopandas as gpd
from green_potential.exceptions import EmptyDataError, MissingColumnError
from loguru import logger


def coverage_ratio(
    districts_gdf: gpd.GeoDataFrame,
    buildings_gdf: gpd.GeoDataFrame,
    score_column: str = "total_score",
    min_score: float = 0.33,
) -> gpd.GeoDataFrame:
    """Доля зданий с потенциалом озеленения выше порога по каждому району.

    Args:
        districts_gdf: GeoDataFrame административных районов с геометрией.
        buildings_gdf: GeoDataFrame зданий со столбцом оценки.
        score_column: Имя столбца с баллом потенциала.
        min_score: Минимальный балл для учёта здания как «потенциального».

    Returns:
        GeoDataFrame районов с добавленными столбцами:
        ``total_buildings``, ``potential_buildings``, ``coverage_ratio``.

    Raises:
        EmptyDataError: Если один из входных GeoDataFrame пуст.
        MissingColumnError: Если score_column отсутствует в buildings_gdf.

    Example:
        >>> ratio = coverage_ratio(districts, scored_buildings)
        >>> ratio[["name", "coverage_ratio"]].head()
    """
    if districts_gdf.empty:
        raise EmptyDataError("GeoDataFrame районов пуст")
    if buildings_gdf.empty:
        raise EmptyDataError("GeoDataFrame зданий пуст")
    if score_column not in buildings_gdf.columns:
        raise MissingColumnError(f"В данных зданий нет столбца '{score_column}'")

    # Приводим к одному CRS
    if buildings_gdf.crs != districts_gdf.crs:
        logger.info(
            "Перепроецируем здания из {} в {}", buildings_gdf.crs, districts_gdf.crs
        )
        buildings_gdf = buildings_gdf.to_crs(districts_gdf.crs)

    joined = gpd.sjoin(buildings_gdf, districts_gdf, how="left", predicate="within")

    idx_col = districts_gdf.index.name or "index"
    stats = (
        joined.groupby("index_right")
        .agg(
            total_buildings=(score_column, "count"),
            potential_buildings=(score_column, lambda s: (s >= min_score).sum()),
        )
        .reset_index()
        .rename(columns={"index_right": idx_col})
    )

    result = districts_gdf.copy().reset_index()
    result = result.merge(stats, on=idx_col, how="left")
    result["total_buildings"] = result["total_buildings"].fillna(0).astype(int)
    result["potential_buildings"] = result["potential_buildings"].fillna(0).astype(int)
    result["coverage_ratio"] = (
        result["potential_buildings"]
        / result["total_buildings"].replace(0, float("nan"))
    ).fillna(0.0)

    logger.info(
        "Средняя доля зданий с потенциалом по районам: {:.1%}",
        result["coverage_ratio"].mean(),
    )
    return result


def top_districts(
    districts_gdf: gpd.GeoDataFrame,
    score_column: str = "coverage_ratio",
    n: int = 5,
) -> gpd.GeoDataFrame:
    """Топ-N районов с наибольшим потенциалом озеленения.

    Args:
        districts_gdf: GeoDataFrame районов с числовым столбцом оценки.
        score_column: Столбец для ранжирования.
        n: Количество районов в выборке.

    Returns:
        GeoDataFrame из N лучших районов, отсортированных по убыванию score_column.

    Raises:
        EmptyDataError: Если GeoDataFrame пуст.
        MissingColumnError: Если score_column отсутствует.

    Example:
        >>> best = top_districts(districts_with_ratio, n=3)
        >>> best["name"].tolist()
        ['Центральный', 'Адмиралтейский', 'Василеостровский']
    """
    if districts_gdf.empty:
        raise EmptyDataError("GeoDataFrame районов пуст")
    if score_column not in districts_gdf.columns:
        raise MissingColumnError(f"Столбец '{score_column}' отсутствует в данных")

    result = districts_gdf.nlargest(n, score_column)
    logger.info("Топ-{} районов по '{}' выбрано", len(result), score_column)
    return result
