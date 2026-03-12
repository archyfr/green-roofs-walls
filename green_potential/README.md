# green_potential

Библиотека для оценки потенциала озеленения зданий: зелёные крыши и вертикальные системы озеленения в городах с учётом холодного климата.

Разработана в рамках научной работы по теме «Генеративный алгоритм оценки потенциала размещения зелёных крыш и вертикальных систем озеленения в холодных регионах России».

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Быстрый старт

```python
from green_potential import load_buildings, BuildingScorer, filter_greenable_roofs

# Загрузка данных
buildings = load_buildings("data/roofshape.gpkg")

# Фильтрация зданий с подходящими крышами
greenable = filter_greenable_roofs(buildings, roof_column="roof:shape")

# Оценка и классификация потенциала
scorer = BuildingScorer(greenable, roof_column="roof:shape")
classified = scorer.classify()

# Результат: столбцы roof_score, wall_score, total_score, potential_class
print(classified[["roof_area_m2", "total_score", "potential_class"]].head())
```

## Структура проекта

```
green_potential/
├── requirements.txt
├── README.md
├── .pre-commit-config.yaml
└── src/
    └── green_potential/
        ├── __init__.py          # публичный API
        ├── exceptions.py        # пользовательские исключения
        ├── core/
        │   ├── loader.py        # загрузка геоданных
        │   └── filters.py       # фильтрация по атрибутам
        ├── services/
        │   ├── potential.py     # оценка потенциала (BuildingScorer)
        │   └── spatial.py       # пространственный анализ
        └── utils/
            └── crs.py           # работа с системами координат
```

## Публичный API

### Загрузка данных
- `load_buildings(path)` — загружает .gpkg/.shp, фильтрует невалидную геометрию

### Фильтрация
- `filter_by_roof_type(gdf, roof_type)` — фильтр по конкретному типу крыши
- `filter_greenable_roofs(gdf)` — только flat и shed (пригодны для озеленения)
- `sort_by_year(gdf)` — сортировка по году постройки
- `buildings_without_year(gdf)` — здания без даты постройки

### Оценка потенциала
- `BuildingScorer(buildings_gdf)` — класс оценки:
  - `.score()` — добавляет столбцы `roof_score`, `wall_score`, `total_score`
  - `.classify()` — добавляет `potential_class`: `low / medium / high`

### Пространственный анализ
- `coverage_ratio(districts_gdf, buildings_gdf)` — доля зданий с потенциалом по районам
- `top_districts(districts_gdf, n=5)` — топ районов по потенциалу

### Утилиты
- `ensure_metric_crs(gdf)` — привести к метрической проекции
- `assert_same_crs(gdf1, gdf2)` — проверить совпадение CRS

## Исключения

| Исключение | Когда вызывается |
|---|---|
| `EmptyDataError` | GeoDataFrame пуст после фильтрации |
| `InvalidGeometryError` | Нет столбца geometry или геометрия невалидна |
| `MissingColumnError` | Отсутствует обязательный столбец |
| `InvalidRoofTypeError` | Недопустимый тип крыши |
| `InvalidYearError` | Нечисловые значения года постройки |

## Настройка pre-commit

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```
