from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "players" ADD "password" VARCHAR(128);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "players" DROP COLUMN "password";"""
