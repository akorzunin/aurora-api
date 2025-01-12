from functools import partial

from tortoise.contrib.fastapi import RegisterTortoise

from internal.settings import DB_URL

register_orm = partial(
    RegisterTortoise,
    db_url=DB_URL,
    modules={"models": ["internal.db.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": ["internal.db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
