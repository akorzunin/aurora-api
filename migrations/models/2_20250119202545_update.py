from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "tours" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(2000) NOT NULL,
    "text_mini" VARCHAR(2000) NOT NULL,
    "text" TEXT NOT NULL,
    "text_head" VARCHAR(2000) NOT NULL,
    "price" REAL NOT NULL,
    "url" VARCHAR(2000) NOT NULL,
    "image" VARCHAR(2000) NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "tours";"""
