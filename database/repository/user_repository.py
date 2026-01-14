from typing import Any, List, Sequence

from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from ..models import User


class UserRepository:
    """
    Репозиторий для работы с пользователями
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, max_id: int, full_name: str, username: str = None, campaign_id: int = 0) -> User | str:
        """Создать нового пользователя"""
        user_data = await UserRepository.get_user_by_telegram_id(self, max_id)
        if not user_data:
            user = User(
                max_id=int(max_id),
                username=username,
                full_name=full_name,
                campaign_id=campaign_id
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        else:
            if campaign_id:
                user_data.campaign_id = int(campaign_id)
                await self.session.commit()
                await self.session.refresh(user_data)
                return user_data
            else:
                return "ok"

    async def get_user_by_telegram_id(self, max_id: int) -> User | None:
        """Найти пользователя по telegram_id"""
        result = await self.session.execute(
            select(User).where(User.max_id == int(max_id))
        )
        return result.scalars().first()

    async def get_users(self) -> Sequence[Any]:
        """Найти пользователей для рассылки"""
        result = await self.session.execute(
            select(User.username)
        )
        return result.scalars().all()

    async def get_users_by_campaign_id(self, campaign_id) -> Sequence[Any]:
        """Найти пользователей для рассылки"""
        result = await self.session.execute(
            select(User.username).where(User.campaign_id == int(campaign_id))
        )
        return result.scalars().all()