from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "customers" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "current_geo_lat" REAL,
    "current_geo_long" REAL,
    "selected_geo_lat" REAL NOT NULL,
    "selected_geo_long" REAL NOT NULL,
    "locale" VARCHAR(2) NOT NULL  DEFAULT 'ru',
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "subscriptions" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "cust_name" VARCHAR(255) NOT NULL,
    "cust_surname" VARCHAR(255),
    "cust_patronymic" VARCHAR(255),
    "alert_probability" INT NOT NULL,
    "sub_type" INT NOT NULL,
    "geo_push_type" VARCHAR(255) NOT NULL,
    "active" INT NOT NULL  DEFAULT 0,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "cust_id" INT NOT NULL REFERENCES "customers" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
