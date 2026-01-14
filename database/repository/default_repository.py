from typing import Any, List, Sequence

from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Default


class DefaultRepository:
    """
    Репозиторий для работы с дефолтными значениями
    """
    def __init__(self, session: AsyncSession):
        self.session = session


    async def update_default_value(
            self,
            name: str,
            value: str
    ) -> Default | None:
        """Изменить значение дефолтного ключа"""

        result = await self.session.execute(select(Default).where(Default.name == name))
        res: Default = result.scalar_one_or_none()

        if not res:
            return None

        res.value = value

        await self.session.commit()
        await self.session.refresh(res)
        return res



    async def get_value(self,
                        name:str
                        ) -> Sequence[Any]:
        """Найти значение для дефолта"""
        result = await self.session.execute(
            select(Default.value).where(Default.name == name)
        )
        return result.scalar_one_or_none()