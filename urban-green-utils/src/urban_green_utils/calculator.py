from typing import Optional


def green_roof_potential(
    roof_area_m2: float,
    slope_deg: float = 0.0,
    load_capacity_kpa: Optional[float] = None,
) -> dict:
    if roof_area_m2 <= 0:
        raise ValueError("Площадь крыши должна быть положительной")
    if not (0 <= slope_deg <= 45):
        raise ValueError("Уклон должен быть от 0 до 45 градусов")

    if slope_deg > 30:
        roof_type = "не рекомендуется"
        score = 0.0
    elif slope_deg > 15:
        roof_type = "экстенсивная"
        score = 0.4
    else:
        if load_capacity_kpa is not None and load_capacity_kpa >= 4.5:
            roof_type = "интенсивная"
            score = 1.0
        else:
            roof_type = "экстенсивная"
            score = 0.7

    usable_area = roof_area_m2 * max(0.0, 1 - slope_deg / 45)

    return {
        "recommended_type": roof_type,
        "potential_score": round(score, 2),
        "usable_area_m2": round(usable_area, 2),
        "co2_offset_kg_per_year": round(usable_area * 0.5 * score, 2),
    }


def vertical_garden_potential(
    wall_area_m2: float,
    orientation: str = "south",
    sunlight_hours: float = 6.0,
) -> dict:
    orientation_factor = {
        "south": 1.0,
        "east": 0.8,
        "west": 0.75,
        "north": 0.4,
    }
    factor = orientation_factor.get(orientation.lower(), 0.6)
    score = min(1.0, (sunlight_hours / 8) * factor)

    return {
        "orientation_factor": factor,
        "potential_score": round(score, 2),
        "recommended": score >= 0.5,
        "estimated_plants": int(wall_area_m2 * 4 * score),
    }