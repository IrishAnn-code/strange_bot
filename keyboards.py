from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_kb = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')],
        [KeyboardButton(text='Регистрация'), KeyboardButton(text='Купить')]
    ], resize_keyboard=True
)

kb_inline = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text='Формула расчёта', callback_data='info'),
        InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calc')]
    ]
)

kb_buy = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Маленький', callback_data='product_buying'),
        InlineKeyboardButton(text='Средний', callback_data='product_buying'),
        InlineKeyboardButton(text='Большой', callback_data='product_buying'),
        InlineKeyboardButton(text='Акция', callback_data='product_buying')]
    ]
)
