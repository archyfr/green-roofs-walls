# urban-green-utils

Библиотека для оценки потенциала зелёных крыш и вертикальных садов в городской среде.

## Установка

    pip install urban-green-utils

Пакет доступен на PyPI: https://pypi.org/project/urban-green-utils/

## Пример использования

    from urban_green_utils import green_roof_potential, vertical_garden_potential

    # Оценка зелёной крыши
    result = green_roof_potential(
        roof_area_m2=500,
        slope_deg=5,
        load_capacity_kpa=5.0
    )
    print(result)
    # {'recommended_type': 'интенсивная', 'potential_score': 1.0,
    #  'usable_area_m2': 444.44, 'co2_offset_kg_per_year': 222.22}

    # Оценка вертикального сада
    vg = vertical_garden_potential(
        wall_area_m2=100,
        orientation="south",
        sunlight_hours=7
    )
    print(vg)
    # {'orientation_factor': 1.0, 'potential_score': 0.88,
    #  'recommended': True, 'estimated_plants': 350}

## Функции

### green_roof_potential

Оценивает потенциал зелёной крыши по параметрам здания.

Параметры:
- roof_area_m2 — площадь крыши в м²
- slope_deg — уклон крыши в градусах (0-45)
- load_capacity_kpa — несущая способность в кПа (опционально)

Возвращает тип озеленения, оценку потенциала, полезную площадь и CO2-эффект.

### vertical_garden_potential

Оценивает потенциал вертикального озеленения стены.

Параметры:
- wall_area_m2 — площадь стены в м²
- orientation — ориентация стены (north/south/east/west)
- sunlight_hours — часов солнца в день

Возвращает коэффициент ориентации, оценку потенциала, рекомендацию (True/False) и примерное количество растений.

## Ссылки

- PyPI: https://pypi.org/project/urban-green-utils/
- GitHub: https://github.com/archyfr/green-roofs-walls