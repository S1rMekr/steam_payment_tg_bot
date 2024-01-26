from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Оплатить стим')],
        [KeyboardButton(text='Помощь')]
        ], resize_keyboard=True, one_time_keyboard=True)

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отмена')]
    ],resize_keyboard=True, one_time_keyboard=True)

login_confirm_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Да',callback_data='login_confirmed')],
        [InlineKeyboardButton(text='Нет', callback_data='login_canceled')]
        ])

async def prices():
    prices_kb = InlineKeyboardBuilder()
    prices_kb.add(
        InlineKeyboardButton(text='100', callback_data='100'),
        InlineKeyboardButton(text='500', callback_data='500'),
        InlineKeyboardButton(text='1000', callback_data='1000'),
        InlineKeyboardButton(text='2000', callback_data='2000'),
        )
    return prices_kb.adjust(2).as_markup()

