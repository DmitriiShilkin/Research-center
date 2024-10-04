import uuid
from typing import Optional
from uuid import UUID

from configs.db import close_db, init_db
from crud.async_crud import BaseAsyncCRUD
from models import User
from schemas.user import UserCreate, UserUpdateDB
from security.password import hash_password


class CRUDUser(BaseAsyncCRUD[User, UserCreate, UserUpdateDB]):
    async def get_by_uid(self, uid: UUID) -> Optional[User]:
        return await self.model.filter(uid=uid).first()

    async def get_by_email(
        self, email: str
    ) -> Optional[User]:
        await init_db()
        obj = await self.model.filter(email=email).first()
        await close_db()

        return obj

    async def create(
        self,
        *,
        create_data: UserCreate,
    ) -> User:
        await init_db()
        try:
            create_data = create_data.model_dump(exclude_unset=True)
            hashed_password = await hash_password(create_data.pop("password"))
            random_uid = str(uuid.uuid4())
            user_created = await User.create(
                uid=random_uid,
                username=create_data.get("email").split('@')[0],
                hashed_password=hashed_password,
                **create_data,
            )
        except Exception:
            raise
        await close_db()

        return user_created


crud_user = CRUDUser(User)
