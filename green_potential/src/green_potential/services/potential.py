"""Оценка потенциала озеленения зданий: зелёные крыши и вертикальное озеленение."""

import geopandas as gpd
import pandas as pd
from green_potential.exceptions import EmptyDataError
from loguru import logger

# Минимальная площадь кровли для размещения зелёной крыши (м²)
MIN_ROOF_AREA_M2 = 50.0

# Минимальный периметр здания для вертикального озеленения (м)
MIN_PERIMETER_M = 20.0

# Типы крыш, пригодных для зелёной кровли
SUITABLE_ROOF_TYPES: set[str] = {"flat", "shed"}


class BuildingScorer:
    """Оценка потенциала озеленения отдельного здания или набора зданий.

    Вычисляет балл от 0 до 1 на основе:
    - типа крыши,
    - площади кровли,
    - периметра здания (для фасадного озеленения).

    Args:
        buildings_gdf: GeoDataFrame зданий в метрической проекции (например, EPSG:32636).
        roof_column: Имя столбца с типом крыши.

    Example:
        >>> scorer = BuildingScorer(buildings, roof_column="roof:shape")
        >>> scored = scorer.score()
        >>> classified = scorer.classify()
    """

    def __init__(
        self,
        buildings_gdf: gpd.GeoDataFrame,
        roof_column: str = "roof:shape",
    ) -> None:
        if buildings_gdf.empty:
            raise EmptyDataError("Передан пустой GeoDataFrame зданий")
        self._gdf = buildings_gdf.copy()
        self._roof_column = roof_column
        self._ensure_metric_crs()

    def _ensure_metric_crs(self) -> None:
        """Приводит данные к метрической проекции при необходимости."""
        if self._gdf.crs is None:
            logger.warning(
                "CRS не задан, предполагается EPSG:4326 → перепроецируем в EPSG:32636"
            )
            self._gdf = self._gdf.set_crs(4326).to_crs(32636)
        elif self._gdf.crs.is_geographic:
            logger.info(
                "Перепроецируем из {} в EPSG:32636 для расчётов площади", self._gdf.crs
            )
            self._gdf = self._gdf.to_crs(32636)

    def score(self) -> gpd.GeoDataFrame:
        """Вычислить балл потенциала озеленения для каждого здания.

        Добавляет столбцы:
        - ``roof_area_m2`` — площадь кровли (м²),
        - ``perimeter_m`` — периметр здания (м),
        - ``roof_score`` — балл зелёной крыши [0..1],
        - ``wall_score`` — балл вертикального озеленения [0..1],
        - ``total_score`` — итоговый балл [0..1].

        Returns:
            GeoDataFrame с добавленными столбцами оценки.

        Example:
            >>> scored = scorer.score()
            >>> scored["total_score"].mean()
            0.43
        """
        result = self._gdf.copy()

        result["roof_area_m2"] = result.geometry.area
        result["perimeter_m"] = result.geometry.length

        result["roof_score"] = self._calc_roof_score(result)
        result["wall_score"] = self._calc_wall_score(result)
        result["total_score"] = (result["roof_score"] + result["wall_score"]) / 2

        logger.info(
            "Оценка завершена: средний балл {:.2f} по {} зданиям",
            result["total_score"].mean(),
            len(result),
        )
        return result

    def classify(self) -> gpd.GeoDataFrame:
        """Классифицировать здания по потенциалу озеленения.

        Добавляет столбец ``potential_class``:
        - ``"high"`` — total_score ≥ 0.66,
        - ``"medium"`` — total_score ≥ 0.33,
        - ``"low"`` — total_score < 0.33.

        Returns:
            GeoDataFrame с добавленным столбцом классификации.

        Example:
            >>> classified = scorer.classify()
            >>> classified["potential_class"].value_counts()
            medium    512
            low       301
            high       89
        """
        scored = self.score()

        conditions = [
            scored["total_score"] >= 0.66,
            scored["total_score"] >= 0.33,
        ]
        choices = ["high", "medium"]
        scored["potential_class"] = pd.Series(
            pd.Categorical(
                [
                    choices[0] if c[0] else choices[1] if c[1] else "low"
                    for c in zip(*conditions)
                ],
                categories=["low", "medium", "high"],
                ordered=True,
            ),
            index=scored.index,
        )

        counts = scored["potential_class"].value_counts()
        logger.info(
            "Классификация: high={}, medium={}, low={}",
            counts.get("high", 0),
            counts.get("medium", 0),
            counts.get("low", 0),
        )
        return scored

    def _calc_roof_score(self, gdf: gpd.GeoDataFrame) -> pd.Series:
        """Балл зелёной крыши на основе типа и площади."""
        has_suitable_type = (
            gdf[self._roof_column].isin(SUITABLE_ROOF_TYPES)
            if self._roof_column in gdf.columns
            else pd.Series(False, index=gdf.index)
        )
        area_score = (gdf["roof_area_m2"] - MIN_ROOF_AREA_M2).clip(lower=0)
        area_score = (area_score / (area_score.max() or 1)).clip(0, 1)

        return (has_suitable_type.astype(float) * 0.6 + area_score * 0.4).clip(0, 1)

    def _calc_wall_score(self, gdf: gpd.GeoDataFrame) -> pd.Series:
        """Балл вертикального озеленения на основе периметра."""
        perim_score = (gdf["perimeter_m"] - MIN_PERIMETER_M).clip(lower=0)
        return (perim_score / (perim_score.max() or 1)).clip(0, 1)
