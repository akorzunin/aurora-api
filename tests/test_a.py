from unittest.mock import patch

import pytest
from tortoise.contrib.test import init_memory_sqlite

from internal.db.models import Customers


@pytest.fixture(scope="session", autouse=True)
def db_init():
    with patch("internal.settings.DB_URL", "sqlite://:memory:") as _:
        yield


@pytest.mark.asyncio
@init_memory_sqlite(models=["internal.db.models", "aerich.models"])
async def test_run():
    c = await Customers.create(
        selected_geo_lat=1,
        selected_geo_long=2,
    )
    assert c
