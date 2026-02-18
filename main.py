import geopandas as gpd
from utils import load_buildings, sort_by_year, buildings_without_year, filter_by_roof_type

from pathlib import Path

def main():
    project_root = Path(__file__).resolve().parent 
    shp_path = project_root / "roofshape.gpkg"      
    buildings = load_buildings(shp_path)

    print(f"Загружено {len(buildings)} зданий")
    print("Название столбцов:", buildings.columns.tolist())
    print()

# 2. Фильтрация по типу крыши
    if "roof:shape" in buildings.columns:
        flat_roofs = filter_by_roof_type(buildings, "flat", roof_column="roof:shape")
        gable_roofs = filter_by_roof_type(buildings, "gabled", roof_column="roof:shape") 

    print(f"Плоских крыш (roof:shape='flat'): {len(flat_roofs)}")
    print(f"Двускатных (roof:shape='gabled'): {len(gable_roofs)}")
    print()

    if "start_date" in buildings.columns:
    # 3. Сортировка по году
        by_year = sort_by_year(buildings, year_column="start_date", ascending=True)
    print("Самые старые здания (по start_date):")
    print(by_year[["start_date", "roof:shape", "building"]].head())
    print()

    # 4. Здания «без года»
    no_year = buildings_without_year(buildings, year_column="start_date")
    print(f"Без года постройки (start_date is NaN): {len(no_year)}")
    print()

# 5. Сохранение результатов в файлы
    buildings.to_file("buildings_spb.gpkg", driver="GPKG")
    buildings.drop(columns="geometry").to_csv("buildings_spb.csv", index=False)

    print(f"Result: {len(buildings)} зданий загружено и обработано")

if __name__ == "__main__":
  main()

