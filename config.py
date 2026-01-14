from dataclasses import dataclass
from environs import Env
from maxapi import Dispatcher

dp = Dispatcher()

@dataclass
class MaxBot:
    token: str
    admin_ids: list[int]


@dataclass
class WebApp:
    url: str


@dataclass
class DbConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )

@dataclass
class Api:
    api_url: str
    service_code: str

@dataclass
class Config:
    max_bot: MaxBot
    db: DbConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        max_bot=MaxBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMIN_IDS")))
        ),
        db=DbConfig(
            host=env.str("DB_HOST"),
            port=env.int("DB_PORT"),
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD"),
            database=env.str("DB_NAME"),
        )
    )
