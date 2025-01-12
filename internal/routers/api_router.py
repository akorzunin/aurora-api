from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Body, Response
from pydantic import AwareDatetime, BaseModel

from internal.db.models import Cities
from internal.db.schemas import City
from internal.nooa import nooa_req, swpc_req
from internal.nooa.calc import AuroraProbabilityCalculation, aurora_probability

router = APIRouter(
    prefix="/api/v1",
    tags=["API"],
)


class AuroraProbabilityBody(BaseModel):
    local_time: AwareDatetime = datetime.now(timezone.utc)
    lat: float
    lon: float
    speed: float = 450
    clouds: float = 30


UserBody = Annotated[
    AuroraProbabilityBody,
    Body(
        openapi_examples={
            "Murmansk": {
                "value": {
                    "lat": 68.9792,
                    "lon": 33.0925,
                }
            },
            "Kirov": {
                "value": {
                    "lat": 58.6,
                    "lon": 49.6,
                }
            },
            "Moscow": {
                "value": {
                    "local_time": "2023-03-01T00:00:00+03:00",
                    "lat": 55.75,
                    "lon": 37.62,
                    "speed": 450,
                    "clouds": 30,
                }
            },
        }
    ),
]


class SwpcApiData(BaseModel):
    dst: swpc_req.SwpcDstReq
    bz: swpc_req.SwpcBzReq
    kp: swpc_req.SwpcKpReq


class AuroraProbabilityResponse(BaseModel):
    calc_data: AuroraProbabilityCalculation
    user_data: AuroraProbabilityBody
    api_data: SwpcApiData


@router.post(
    "/aurora-probabilitiy",
    response_model=AuroraProbabilityResponse,
)
async def api_aurora_probability(
    ub: UserBody,
    dst: swpc_req.DstDep,
    bz: swpc_req.BzDep,
    kp: swpc_req.KpDep,
):
    """Получение вероятности северного сияния по заданным параметрам"""
    ad = SwpcApiData(dst=dst, bz=bz, kp=kp)
    res = aurora_probability(
        user_data=ub,
        dst=ad.dst,
        bz=ad.bz,
        kp=ad.kp,
        speed=ub.speed,
        clouds=ub.clouds,
    )

    return AuroraProbabilityResponse(
        calc_data=res,
        user_data=ub,
        api_data=ad,
    )


@router.get("/aurora-map", response_model=nooa_req.NooaAuroraReq)
async def api_aurora_map(aurora_res: nooa_req.AuroraDep):
    """Получение карты северного сияния"""
    return Response(content=aurora_res, media_type="application/json")


@router.get("/aurora-kp-3", response_model=nooa_req.NooaAuroraKp3Req)
async def api_aurora_kp_3(aurora_kp_res: nooa_req.Kp3Dep):
    """Получение планетарного k-индекса за 3 дня"""
    return aurora_kp_res


@router.get("/aurora-kp-27", response_model=nooa_req.NooaAuroraKp27Req)
async def api_aurora_kp_map(aurora_kp_res: nooa_req.Kp27Dep):
    """Получение планетарного k-индекса за 27 дней"""
    return aurora_kp_res


@router.get("/all-cities", response_model=list[City])
async def api_all_cities():
    """Получение списка всех городов для выбора"""
    return await Cities.all()