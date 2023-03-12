from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "images" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "image_key" UUID NOT NULL,
    "name" TEXT NOT NULL
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "images";"""
