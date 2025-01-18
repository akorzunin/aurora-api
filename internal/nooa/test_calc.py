from internal.nooa.calc import nearst_aurora_probability
from internal.nooa.nooa_req import NooaAuroraRes
from internal.routers.api_router import NooaAuroraReq


def test_nearest_aurora():
    prob_map = nearst_aurora_probability(
        pos=NooaAuroraReq(
            lat=55.75,
            lon=37.62,
        ),
        prob_map=NooaAuroraRes(
            Observation_Time="2025-01-11T15:06:00Z",
            Forecast_Time="2025-01-11T16:06:00Z",
            Data_Format="[Longitude, Latitude, Aurora]",
            coordinates=[
                [36 + 180, 54, 3],
                [37 + 180, 55, 4],
                [38 + 180, 56, 5],
            ],
        ),
    )
    assert prob_map.probability == 5
    assert prob_map.lat == 56
    assert prob_map.lon == 38
