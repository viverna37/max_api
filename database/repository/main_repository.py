from sqlalchemy.ext.asyncio import AsyncSession

from .campaign_repository import CampaignRepository
from .default_repository import DefaultRepository
from .user_repository import UserRepository


class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session)
        self.default_repository = DefaultRepository(session)
        self.campaign_repository = CampaignRepository(session)