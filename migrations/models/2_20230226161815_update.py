from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "players" ADD "telegram_id" INT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "players" DROP COLUMN "telegram_id";"""
