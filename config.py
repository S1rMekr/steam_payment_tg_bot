from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str
    payment_token: str
    
@dataclass
class Config:
    tg_bot: TgBot

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'), payment_token=env('PAYMENT_TOKEN')))