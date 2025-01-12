import structlog
from fastapi import APIRouter, Depends

from internal.auth import check_credentials
from internal.db.models import Cities, Customers
from internal.db.schemas import City, CityIn, Cust

logger = structlog.stdlib.get_logger(__name__)
router = APIRouter(
    prefix="/api/v1",
    tags=["Admin"],
    dependencies=[Depends(check_credentials)],
)


@router.get("/all-customers", response_model=list[Cust])
async def all_customers():
    ac = await Customers.all()
    return ac


@router.post("/set-cities", response_model=list[City])
async def set_cities(cities: list[CityIn]):
    res = await Cities.all().delete()
    logger.info(f"Deleted cities: {res} ", count=res)
    cs = []
    for c in cities:
        nc = await Cities.create(**c.model_dump())
        cs.append(nc)
    return cs
