from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "players" ADD "password" VARCHAR(128) NOT NULL  DEFAULT 'Пусто';
        ALTER TABLE "players" ADD "telegram_id" INT  UNIQUE;
        CREATE UNIQUE INDEX "uid_players_telegra_9e1e56" ON "players" ("telegram_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_players_telegra_9e1e56";
        ALTER TABLE "players" DROP COLUMN "password";
        ALTER TABLE "players" DROP COLUMN "telegram_id";"""
