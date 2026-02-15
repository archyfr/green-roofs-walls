import geopandas as gpd

def load_buildings(path: str) -> gpd.GeoDataFrame:
    """Загрузка геоданных зданий и фильтрация невалидной геометрии."""
    gdf = gpd.read_file(path)
    return gdf[gdf.geometry.is_valid]

def sort_by_year(gdf: gpd.GeoDataFrame, year_column: str = "year_built", ascending: bool = True) -> gpd.GeoDataFrame:
    """Сортировка по году постройки."""
    return gdf.sort_values(year_column, ascending=ascending)

def buildings_without_year(gdf: gpd.GeoDataFrame, year_column = "type"):
    """Здания без информации о годе постройки."""
    return gdf[gdf[year_column].isna()]


def filter_by_roof_type(gdf: gpd.GeoDataFrame, roof_type: str, roof_column: str = "roof_type") -> gpd.GeoDataFrame:
    """Фильтрация зданий по типу крыши в столбце roof_column."""
    return gdf[gdf[roof_column] == roof_type]








