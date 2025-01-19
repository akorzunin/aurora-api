import structlog
from fastapi import APIRouter, Depends, HTTPException

from internal.auth import check_credentials
from internal.db.models import Cities, Customers, Tours
from internal.db.schemas import City, CityIn, Cust, Message, Tour, TourIn
from internal.nooa import nooa_req, swpc_req

logger = structlog.stdlib.get_logger(__name__)
router = APIRouter(
    prefix="/api/v1",
    tags=["Admin"],
    dependencies=[Depends(check_credentials)],
)


@router.get("/all-customers", response_model=list[Cust])
async def all_customers():
    """Получение списка всех пользователей"""
    ac = await Customers.all()
    return ac


@router.post("/set-cities", response_model=list[City])
async def set_cities(cities: list[CityIn]):
    """Перезапись списка городов"""
    res = await Cities.all().delete()
    logger.info(f"Deleted cities: {res} ", count=res)
    cs = []
    for c in cities:
        nc = await Cities.create(**c.model_dump())
        cs.append(nc)
    return cs


@router.delete("/drop-cache")
async def drop_cache():
    """Очистка кэша запросов в NOOA"""
    swpc_req.storage._cache.cache = {}
    nooa_req.storage._cache.cache = {}
    nooa_req.long_storage._cache.cache = {}
    return {"message": "ok"}


@router.post("/tour", response_model=Tour)
async def set_tour(tour: TourIn):
    """Добавление тура"""
    t = await Tours.create(**tour.model_dump())
    return t


@router.delete(
    "/tour/{tour_id}",
    responses={
        200: {"model": Message},
        404: {"model": Message},
    },
)
async def drop_tour(tour_id: int):
    """Удаление тура"""
    t = await Tours.get_or_none(id=tour_id)
    if t is None:
        raise HTTPException(status_code=404, detail="Tour not found")
    await t.delete()
    return Message(detail="ok")
