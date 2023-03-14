from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "files" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "file_key" UUID NOT NULL,
    "name" TEXT NOT NULL,
    "file_format" VARCHAR(4) NOT NULL,
    "content_type" VARCHAR(255) NOT NULL
);;
        DROP TABLE IF EXISTS "images";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "files";"""
