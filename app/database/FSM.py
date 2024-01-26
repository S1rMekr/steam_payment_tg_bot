from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.fsm.state import State, StatesGroup
redis = Redis(host='localhost')

storage = RedisStorage(redis=redis)

user_dict: dict[int, dict[str, str | int | bool]] = {}

class FSMSteamPay(StatesGroup):
    login = State()
    payment = State()