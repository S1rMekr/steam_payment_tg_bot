from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.types import (Message, LabeledPrice, PreCheckoutQuery, 
                            CallbackQuery, ReplyKeyboardRemove)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from app.keyboard import start_keyboard, login_confirm_kb, cancel_keyboard, prices
from config import Config, load_config
from app.lexicon import LEXICON
from app.database.FSM import FSMSteamPay

from app.database.utils import update_user_in_db

router = Router()

config: Config = load_config()

@router.message(CommandStart(), StateFilter(default_state))
async def start_command(message: Message):
    await message.answer(LEXICON['/start'], reply_markup=start_keyboard)

@router.message(F.text.lower() == 'помощь')
async def help_command(message: Message):
    await message.answer(LEXICON['/help'], reply_markup=start_keyboard)

@router.message(F.text.lower() == 'отмена', ~StateFilter(default_state))
async def cancel_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/cancel'], reply_markup=start_keyboard)
    await state.clear()

@router.message(F.text == 'Оплатить стим', StateFilter(default_state))
async def steam_payment(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['login_required'], reply_markup=cancel_keyboard)
    await state.set_state(FSMSteamPay.login)

@router.message(StateFilter(FSMSteamPay.login))
async def login(message:Message):
    if len(message.text.split()) == 1:
        await message.answer(text=f'Ваш логин <i><b>{message.text}</b></i>?',reply_markup=login_confirm_kb)
    else:
        await message.answer(text=LEXICON['login_error'])
    
@router.callback_query(F.data.in_(['login_confirmed']), StateFilter(FSMSteamPay.login))
async def login_confirmed(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=None)
    await callback.message.answer(text='Введите сумму для оплаты', reply_markup=await prices())
    await state.set_state(FSMSteamPay.payment)

@router.callback_query(F.data.in_(['login_canceled']), StateFilter(FSMSteamPay.login))
async def login_confirmed(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=None)
    await callback.message.answer(text=LEXICON['login_required'])
    await callback.answer()



@router.message(F.text.regexp(r"^(\d+)$").as_("digits"), StateFilter(FSMSteamPay.payment))
async def buy_command(message: Message, bot: Bot):
    price = message.text
    if int(price) in range(1,1000):
        await bot.send_invoice(
            chat_id=message.chat.id,
            title="Пополнение вашего аккаунта",
            description=f"Ваш аккаунт(user_login)",
            payload="test-invoice-payload",
            provider_token=config.tg_bot.payment_token,
            currency="RUB",
            prices=[
                LabeledPrice(
                    label="Пополнение стима",
                    amount=int(price)*100),
            ],
            max_tip_amount=5000,
            suggested_tip_amounts=[2000, 3000, 4000, 5000],
            )

@router.callback_query(F.data.in_(['100','500','1000','2000']), StateFilter(FSMSteamPay.payment))
async def buy_command_btn(callback: CallbackQuery, state: FSMContext, bot: Bot):
    price = callback.data
    if int(price) in range(1,1000):
        await bot.send_invoice(
            chat_id=callback.message.chat.id,
            title="Пополнение вашего аккаунта",
            description=f"Ваш аккаунт(user_login)",
            payload="test-invoice-payload",
            provider_token=config.tg_bot.payment_token,
            currency="RUB",
            prices=[
                LabeledPrice(
                    label="Пополнение стима",
                    amount=int(price)*100),
            ],
            max_tip_amount=5000,
            suggested_tip_amounts=[2000, 3000, 4000, 5000],
            )

   
                        
@router.pre_checkout_query(StateFilter(FSMSteamPay.payment))
async def pre_checkout_query_handler(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@router.message(F.successful_payment, StateFilter(FSMSteamPay.payment))
async def successful_payment_handler(message: Message, state: FSMContext):
    msg = f'Спасибо за оплату {message.successful_payment.total_amount // 100} {message.successful_payment.currency}'
    await message.answer(text=msg)
    await state.clear()

