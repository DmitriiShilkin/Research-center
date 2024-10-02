import uuid
from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel

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
        return await self.model.filter(email=email).first()

    async def create(
        self,
        *,
        create_data: UserCreate,
    ) -> User:
        try:
            create_data = create_data.model_dump(exclude_unset=True)
            hashed_password = await hash_password(create_data.pop("password"))
            random_uid = str(uuid.uuid4())
            user_created = await User.create(
                uid=random_uid,
                username=random_uid,
                hashed_password=hashed_password,
                **create_data,
            )
        except Exception:
            raise

        return user_created

    async def update(
        self,
        *,
        db_obj: User,
        update_data: Union[UserUpdateDB, dict],
    ) -> User:
        if isinstance(update_data, BaseModel):
            update_data = update_data.model_dump(exclude_unset=True)

        await self.model.filter(id=db_obj.id).update(**update_data)

        return await self.model.get(id=db_obj.id)


crud_user = CRUDUser(User)
