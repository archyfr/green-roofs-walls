from geoalchemy2.elements import WKTElement
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.territories.models import Territory, TerritoryMetric
from app.territories.schemas import (
    TerritoryCreate,
    TerritoryMetricCreate,
    TerritoryMetricUpdate,
    TerritoryUpdate,
)


def _territory_select():
    """Базовый select для территорий с преобразованием геометрии в WKT."""
    return select(
        Territory.id,
        Territory.name,
        Territory.territory_type,
        Territory.level,
        Territory.description,
        func.ST_AsText(Territory.geom).label("geom_wkt"),
        Territory.created_at,
    )


def get_territory(db: Session, territory_id: int):
    """Возвращает территорию по идентификатору или None, если не найдена."""
    stmt = _territory_select().where(Territory.id == territory_id)
    return db.execute(stmt).mappings().first()


def list_territories(db: Session, limit: int = 100, offset: int = 0):
    """Возвращает список территорий с пагинацией."""
    stmt = _territory_select().order_by(Territory.id).limit(limit).offset(offset)
    return db.execute(stmt).mappings().all()


def create_territory(db: Session, data: TerritoryCreate):
    """Создаёт новую территорию и возвращает её."""
    territory = Territory(
        name=data.name,
        territory_type=data.territory_type,
        level=data.level,
        description=data.description,
        geom=WKTElement(data.geom_wkt, srid=4326),
    )
    db.add(territory)
    db.commit()
    db.refresh(territory)
    return get_territory(db, territory.id)


def update_territory(db: Session, territory_id: int, data: TerritoryUpdate):
    """Обновляет поля территории и возвращает обновлённую запись или None."""
    territory = db.get(Territory, territory_id)
    if territory is None:
        return None

    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        if field == "geom_wkt":
            territory.geom = WKTElement(value, srid=4326)
        else:
            setattr(territory, field, value)

    db.commit()
    db.refresh(territory)
    return get_territory(db, territory_id)


def delete_territory(db: Session, territory_id: int) -> bool:
    """Удаляет территорию. Возвращает True при успехе, False если не найдена."""
    territory = db.get(Territory, territory_id)
    if territory is None:
        return False
    db.delete(territory)
    db.commit()
    return True


def list_intersecting_territories(db: Session, wkt: str, limit: int = 100, offset: int = 0):
    """Возвращает территории, геометрия которых пересекается с переданным WKT-полигоном."""
    search_geom = WKTElement(wkt, srid=4326)
    stmt = (
        _territory_select()
        .where(func.ST_Intersects(Territory.geom, search_geom))
        .order_by(Territory.id)
        .limit(limit)
        .offset(offset)
    )
    return db.execute(stmt).mappings().all()


def create_metric(db: Session, territory_id: int, data: TerritoryMetricCreate):
    """Создаёт показатель для территории и возвращает его."""
    metric = TerritoryMetric(
        territory_id=territory_id,
        year=data.year,
        population=data.population,
        area_km2=data.area_km2,
        source=data.source,
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric


def list_metrics_by_territory(db: Session, territory_id: int):
    """Возвращает список показателей территории, отсортированных по году."""
    stmt = (
        select(TerritoryMetric)
        .where(TerritoryMetric.territory_id == territory_id)
        .order_by(TerritoryMetric.year)
    )
    return db.execute(stmt).scalars().all()


def update_metric(db: Session, metric_id: int, data: TerritoryMetricUpdate):
    """Обновляет показатель территории и возвращает обновлённую запись или None."""
    metric = db.get(TerritoryMetric, metric_id)
    if metric is None:
        return None

    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(metric, field, value)

    db.commit()
    db.refresh(metric)
    return metric


def delete_metric(db: Session, metric_id: int) -> bool:
    """Удаляет показатель территории. Возвращает True при успехе, False если не найден."""
    metric = db.get(TerritoryMetric, metric_id)
    if metric is None:
        return False
    db.delete(metric)
    db.commit()
    return True
