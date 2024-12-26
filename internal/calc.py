from datetime import datetime

from pydantic import BaseModel

from internal import swpc_req


# Определение геомагнитной широты
def calculate_geomagnetic_latitude(latitude: float, longitude: float) -> float:
    # Простое преобразование, точный расчет возможен через GeoMag
    return min(latitude + 5, 90)


# Функции расчёта:
# Определение зоны видимости на основе Kp-индекса
def kp_zone(kp: int) -> int:
    kp_zones = {
        1: 67,
        2: 66,
        3: 65,
        4: 60,
        5: 55,
        6: 50,
        7: 45,
        8: 40,
        9: 35,
    }
    return kp_zones.get(kp, 0)


# Вес Bz
def bz_factor(bz: float) -> float:
    if bz < 0:  # Южное направление
        return 1.5 + abs(bz) / 10
    else:  # Северное направление
        return max(0.8, 1.0 - bz / 10)


# Вес по скорости солнечного ветра
def speed_factor(speed: float) -> float:
    return 1.0 if speed > 400 else 0.5


# Вес по Dst-индексу
def dst_factor(dst: float) -> float:
    return 1.2 if dst < -50 else 1.0


# Вес по облачности
def clouds_factor(clouds: float) -> float:
    return 1 - clouds / 100


# Вес времени суток
def time_factor(local_hour: int) -> float:
    return 1.0 if 22 <= local_hour or local_hour <= 2 else 0.5


class AuroraProbabilityCalculation(BaseModel):
    base_probability: float
    bz_weight: float
    speed_weight: float
    dst_weight: float
    clouds_weight: float
    time_weight: float
    probability: float


class AuroraProbabilityRequest(BaseModel):
    local_time: datetime
    lat: float
    lon: float


# Основной расчёт:
def aurora_probability(
    user_data: AuroraProbabilityRequest,
    dst: swpc_req.SwpcDstReq,
    bz: swpc_req.SwpcBzReq,
    kp: swpc_req.SwpcKpReq,
    speed: float,
    clouds: float,
) -> AuroraProbabilityCalculation:
    # Расчёт геомагнитной широты
    geomagnetic_latitude = calculate_geomagnetic_latitude(
        user_data.lat, user_data.lon
    )

    # Зона видимости по Kp-индексу
    visibility_zone = kp_zone(kp.kp)
    base_probability = max(
        0, (100 - (visibility_zone - geomagnetic_latitude)) * 10
    )

    # Весовые коэффициенты
    bz_weight = bz_factor(bz.bz_gse)
    speed_weight = speed_factor(speed)
    dst_weight = dst_factor(dst.dst)
    clouds_weight = clouds_factor(clouds)
    time_weight = time_factor(user_data.local_time.hour)

    # Итоговая вероятность
    probability = (
        base_probability
        * bz_weight
        * speed_weight
        * dst_weight
        * clouds_weight
        * time_weight
    )
    return AuroraProbabilityCalculation(
        base_probability=base_probability,
        bz_weight=bz_weight,
        speed_weight=speed_weight,
        dst_weight=dst_weight,
        clouds_weight=clouds_weight,
        time_weight=time_weight,
        probability=min(probability, 100),
    )
