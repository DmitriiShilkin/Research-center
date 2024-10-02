from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "ratealert" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "key_json" JSONB NOT NULL,
            "created_at" TIMESTAMPTZ NOT NULL
        );
        CREATE TABLE IF NOT EXISTS "user" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "uid" UUID NOT NULL UNIQUE,
            "first_name" VARCHAR(50) NOT NULL,
            "second_name" VARCHAR(50) NOT NULL,
            "username" VARCHAR(50) NOT NULL UNIQUE,
            "email" VARCHAR(255) NOT NULL UNIQUE,
            "hashed_password" VARCHAR(255),
            "is_email_verified" BOOL NOT NULL  DEFAULT False,
            "is_admin" BOOL NOT NULL  DEFAULT False,
            "is_superuser" BOOL NOT NULL  DEFAULT False,
            "registered_at" TIMESTAMPTZ NOT NULL,
            "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
            "last_visited_at" TIMESTAMPTZ,
            "last_password_change_at" TIMESTAMPTZ
        );
        CREATE INDEX IF NOT EXISTS "idx_user_uid_9a9b44" ON "user" ("uid");
        CREATE INDEX IF NOT EXISTS "idx_user_usernam_9987ab" ON "user" ("username");
        CREATE INDEX IF NOT EXISTS "idx_user_email_1b4f1c" ON "user" ("email");
        CREATE TABLE IF NOT EXISTS "aerich" (
            "id" SERIAL NOT NULL PRIMARY KEY,
            "version" VARCHAR(255) NOT NULL,
            "app" VARCHAR(100) NOT NULL,
            "content" JSONB NOT NULL
        );
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "ratealert";
        DROP TABLE IF EXISTS "user";
        DROP INDEX IF EXISTS "idx_user_uid_9a9b44";
        DROP INDEX IF EXISTS "idx_user_usernam_9987ab";
        DROP INDEX IF EXISTS "idx_user_email_1b4f1c";
    """
