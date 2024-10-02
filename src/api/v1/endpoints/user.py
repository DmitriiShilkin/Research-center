from fastapi import APIRouter, HTTPException, status

from crud.user import crud_user
from schemas.user import (
    UserCreate,
    UserResponse,
)

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_data: UserCreate,
):
    user = await crud_user.get_by_email(email=create_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {create_data.email} is already "
            "associated with an account.",
        )
    return await crud_user.create(create_data=create_data)
