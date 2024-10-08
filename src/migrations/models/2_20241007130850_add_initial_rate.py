from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "initialrate" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "name" VARCHAR(7) NOT NULL,
            "value" DOUBLE PRECISION NOT NULL
        );
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "initialrate";"""
