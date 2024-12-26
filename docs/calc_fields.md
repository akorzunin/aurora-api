# Поля для расчета вероятности северного сияния

## Const

speed = 450                 # Скорость солнечного ветра (км/с)
clouds = 30                 # Процент облачности

## From client

local_hour = datetime.now().isoformat()  # Местное время в формате ISO 8601 с оффсетом от UTC
latitude = 65.58            # Географическая широта
longitude = 23.62           # Географическая долгота

## From <https://services.swpc.noaa.gov/json/geospace/geospace_dst_1_hour.json>

needs time_tag (client time) данные по каждой минуте за последний час

dst = -60                   # Dst-индекс

## From <https://services.swpc.noaa.gov/json/dscovr/dscovr_mag_1s.json>

needs time_tag (client time) есть данные по каждой секунде за последние 5 минут
есть bz_gsm и bz_gse

bz = -6                     # Bz в нТл

## From <https://services.swpc.noaa.gov/json/planetary_k_index_1m.json>

kp = 4                      # Текущий Kp-индекс
