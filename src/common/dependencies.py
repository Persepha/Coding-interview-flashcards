from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.types import ModelType


async def get_obj_or_404(
    *, session: AsyncSession, id: int, obj: ModelType
) -> ModelType:
    query = select(obj).where(obj.id == id)
    result = await session.execute(query)

    data = result.scalar()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{obj.__tablename__} with the id {id} is not available",
        )

    return data
