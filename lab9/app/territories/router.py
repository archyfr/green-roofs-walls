from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.common.db import get_db
from app.territories import crud
from app.territories.schemas import (
    TerritoryCreate,
    TerritoryMetricCreate,
    TerritoryMetricRead,
    TerritoryMetricUpdate,
    TerritoryRead,
    TerritoryUpdate,
)

router = APIRouter(prefix="/territories", tags=["Территории"])


@router.post(
    "",
    response_model=TerritoryRead,
    status_code=201,
    summary="Создание территории",
    description="Создаёт новую территорию с пространственной геометрией в формате WKT.",
)
def create_territory(
    data: TerritoryCreate,
    db: Session = Depends(get_db),
) -> TerritoryRead:
    """Создаёт новую территорию."""
    return crud.create_territory(db, data)


@router.get(
    "",
    response_model=list[TerritoryRead],
    summary="Список территорий",
    description="Возвращает список всех территорий с поддержкой пагинации.",
)
def list_territories(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[TerritoryRead]:
    """Возвращает список всех территорий."""
    return crud.list_territories(db, limit=limit, offset=offset)


@router.get(
    "/intersects",
    response_model=list[TerritoryRead],
    summary="Пространственный запрос — пересечение",
    description="Возвращает территории, геометрия которых пересекается с переданным WKT-полигоном.",
)
def list_intersecting_territories(
    wkt: str = Query(description="Геометрия в формате WKT, например POLYGON((...))"),
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[TerritoryRead]:
    """Возвращает территории, пересекающиеся с переданным полигоном."""
    return crud.list_intersecting_territories(db, wkt=wkt, limit=limit, offset=offset)


@router.get(
    "/{territory_id}",
    response_model=TerritoryRead,
    summary="Получение территории по ID",
    description="Возвращает территорию по её идентификатору.",
)
def get_territory(
    territory_id: int,
    db: Session = Depends(get_db),
) -> TerritoryRead:
    """Возвращает территорию по идентификатору."""
    territory = crud.get_territory(db, territory_id)
    if territory is None:
        raise HTTPException(status_code=404, detail="Territory not found")
    return territory


@router.put(
    "/{territory_id}",
    response_model=TerritoryRead,
    summary="Обновление территории",
    description="Обновляет переданные поля территории. Поля, не указанные в запросе, остаются без изменений.",
)
def update_territory(
    territory_id: int,
    data: TerritoryUpdate,
    db: Session = Depends(get_db),
) -> TerritoryRead:
    """Обновляет поля территории."""
    territory = crud.update_territory(db, territory_id, data)
    if territory is None:
        raise HTTPException(status_code=404, detail="Territory not found")
    return territory


@router.delete(
    "/{territory_id}",
    status_code=204,
    summary="Удаление территории",
    description="Удаляет территорию и все связанные с ней показатели.",
)
def delete_territory(
    territory_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Удаляет территорию и все её показатели."""
    deleted = crud.delete_territory(db, territory_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Territory not found")


@router.post(
    "/{territory_id}/metrics",
    response_model=TerritoryMetricRead,
    status_code=201,
    summary="Создание показателя территории",
    description="Добавляет новый показатель для указанной территории.",
)
def create_metric(
    territory_id: int,
    data: TerritoryMetricCreate,
    db: Session = Depends(get_db),
) -> TerritoryMetricRead:
    """Создаёт показатель для территории."""
    territory = crud.get_territory(db, territory_id)
    if territory is None:
        raise HTTPException(status_code=404, detail="Territory not found")
    return crud.create_metric(db, territory_id, data)


@router.get(
    "/{territory_id}/metrics",
    response_model=list[TerritoryMetricRead],
    summary="Список показателей территории",
    description="Возвращает все показатели для указанной территории, отсортированные по году.",
)
def list_metrics(
    territory_id: int,
    db: Session = Depends(get_db),
) -> list[TerritoryMetricRead]:
    """Возвращает показатели территории."""
    territory = crud.get_territory(db, territory_id)
    if territory is None:
        raise HTTPException(status_code=404, detail="Territory not found")
    return crud.list_metrics_by_territory(db, territory_id)


@router.put(
    "/{territory_id}/metrics/{metric_id}",
    response_model=TerritoryMetricRead,
    summary="Обновление показателя территории",
    description="Обновляет переданные поля показателя. Поля, не указанные в запросе, остаются без изменений.",
)
def update_metric(
    territory_id: int,
    metric_id: int,
    data: TerritoryMetricUpdate,
    db: Session = Depends(get_db),
) -> TerritoryMetricRead:
    """Обновляет показатель территории."""
    territory = crud.get_territory(db, territory_id)
    if territory is None:
        raise HTTPException(status_code=404, detail="Territory not found")
    metric = crud.update_metric(db, metric_id, data)
    if metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric


@router.delete(
    "/{territory_id}/metrics/{metric_id}",
    status_code=204,
    summary="Удаление показателя территории",
    description="Удаляет показатель территории по его идентификатору.",
)
def delete_metric(
    territory_id: int,
    metric_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Удаляет показатель территории."""
    territory = crud.get_territory(db, territory_id)
    if territory is None:
        raise HTTPException(status_code=404, detail="Territory not found")
    deleted = crud.delete_metric(db, metric_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Metric not found")
