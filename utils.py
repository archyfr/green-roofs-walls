import geopandas as gpd
from pathlib import Path
from typing import Union


def load_buildings(path: Union[str, Path]) -> gpd.GeoDataFrame:
    """Загрузка геоданных зданий и фильтрация невалидной геометрии.

    Args:
        path (str | Path): Путь до файла с геоданными.

    Returns:
        gpd.GeoDataFrame: GeoDataFrame из прочитанного файла, отфильтрованный по непустым и валидным геометриям. """
    try:
        gdf = gpd.read_file(path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Файл не найден: {path}") from e
    except Exception as e:
        raise RuntimeError(f"Не удалось прочитать файл: {path}") from e

    if "geometry" not in gdf.columns:
        raise ValueError("Данные не содержат столбец 'geometry'")

    gdf = gdf[gdf.geometry.notna()]

    if gdf.empty:
        raise ValueError("После фильтрации пустой геометрии не осталось ни одного здания")

    gdf = gdf[gdf.geometry.is_valid]

    if gdf.empty:
        raise ValueError("После фильтрации невалидной геометрии не осталось ни одного здания")

    return gdf


def sort_by_year(gdf: gpd.GeoDataFrame, year_column: str = "year_built", ascending: bool = True,) -> gpd.GeoDataFrame:
    """Сортировка зданий по году постройки.

    Args:
        gdf (gpd.GeoDataFrame): Таблица зданий.
        year_column (str): Имя столбца с годом постройки.
        ascending (bool): Порядок сортировки (True — по возрастанию).

    Returns:
        gpd.GeoDataFrame: Отсортированный GeoDataFrame."""
    if year_column not in gdf.columns:
        raise KeyError(f"В данных нет столбца '{year_column}' для сортировки по году")

    if (
        not gdf[year_column].empty
        and not gdf[year_column].dropna().map(lambda v: isinstance(v, (int, float))).all()
    ):
        raise TypeError(
            f"Столбец '{year_column}' должен содержать числовые значения (год постройки)"
        )

    return gdf.sort_values(year_column, ascending=ascending)


def buildings_without_year(gdf: gpd.GeoDataFrame, year_column: str = "year_built",) -> gpd.GeoDataFrame:
    """Выборка зданий без информации о годе постройки.

    Args:
        gdf (gpd.GeoDataFrame): Таблица зданий.
        year_column (str): Имя столбца с годом постройки.

    Returns:
        gpd.GeoDataFrame: GeoDataFrame только с записями, где год постройки отсутствует."""
    if year_column not in gdf.columns:
        raise KeyError(f"В данных нет столбца '{year_column}' для поиска пустый ячеек")

    result = gdf[gdf[year_column].isna()]

    if result.empty:
        print(f"В столбце '{year_column}' нет пустых ячеек")

    return result


def filter_by_roof_type(gdf: gpd.GeoDataFrame, roof_type: str, roof_column: str = "roof:shape",) -> gpd.GeoDataFrame:
    """Фильтрация зданий по типу крыши.

    Args:
        gdf (gpd.GeoDataFrame): Таблица зданий.
        roof_type (str): Тип крыши, по которому фильтруем.
        roof_column (str): Имя столбца с типом крыши.

    Returns:
        gpd.GeoDataFrame: GeoDataFrame только со зданиями нужного типа крыши."""
    if roof_column not in gdf.columns:
        raise KeyError(f"В данных нет столбца '{roof_column}' для фильтрации по типу крыши")

    result = gdf[gdf[roof_column] == roof_type]

    if result.empty:
        print(f"Нет зданий с типом крыши '{roof_type}' в столбце '{roof_column}'")

    return result










