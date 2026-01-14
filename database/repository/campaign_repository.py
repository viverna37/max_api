from typing import Any, List, Sequence

from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Campaign


class CampaignRepository:
    """
    Репозиторий для работы с кампаниями
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, links: list[str], start_msg: str) -> Campaign:
        """Создать новую рекламную кампанию"""
        print(links, "перед записью в бд")
        campaign = Campaign(
            name=name,
            message=start_msg,
            links=links
        )
        self.session.add(campaign)
        await self.session.commit()
        await self.session.refresh(campaign)
        return campaign

    async def increment(self, campaign_id: int) -> Campaign | None:
        """Обновить счетчик + 1"""
        result = await self.session.execute(select(Campaign).where(Campaign.id == int(campaign_id)))
        res: Campaign = result.scalar_one_or_none()

        if not res:
            return None

        res.count_transitions = res.count_transitions + 1

        await self.session.commit()
        await self.session.refresh(res)
        return res

    async def get_campaign(self,
                           campaign_id: int
                           ) -> Campaign:
        """Найти кампанию"""
        result = await self.session.execute(
            select(Campaign).where(Campaign.id == int(campaign_id))
        )
        return result.scalar_one_or_none()

    async def get_all_campaigns(self ) -> ScalarResult[Any]:
        """Найти кампанию"""
        result = await self.session.execute(
            select(Campaign)
        )
        return result.scalars()
