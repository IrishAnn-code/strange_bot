from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from crud_functions import initiate_db, get_all_products, initiate_db_Users, add_user, is_included
from keyboards import *
import asyncio
import os

initiate_db(), initiate_db_Users()

TOKEN = ''
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(
        'Привет! Я бот, помогающий твоему здоровью', reply_markup=main_kb)


@dp.message(F.text == 'Рассчитать')
async def kb_inline_start(message: Message):
    await message.answer('Вы можете рассчитать норму калорий и посмотреть формулу расчета',
                         reply_markup=kb_inline)


@dp.callback_query(F.data == "info")
async def handle_info(callback: CallbackQuery):
    await callback.message.answer("Формула для расчета нормы калорий: "
                                  "\n10 х вес(кг) + 6,25 х рост(см) + 5 х возраст(лет) - 161")
    await callback.answer()


@dp.callback_query(F.data == "calc")
async def set_age(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Введите свой возраст:')
    await state.set_state(UserState.age)


@dp.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await state.set_state(UserState.growth)


@dp.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await state.set_state(UserState.weight)


@dp.message(UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    try:
        age = int(data['age'])
        growth = int(data['growth'])
        weight = int(data['weight'])
        calories = 10 * weight + 6.25 * growth - 5 * age - 161
        await message.answer(f'Ваша норма калорий: {calories:.2f}')
    except ValueError:
        await message.answer('Пожалуйста, вводите только числа')
    await state.clear()


@dp.message(F.text == 'Купить')
async def get_buying_list(message: Message):
    get = os.getcwd()
    products = get_all_products()
    for product in products:
        file_path = os.path.join(get, 'pills', f'{product[0]}.jpg')
        try:
            photo = FSInputFile(file_path)
            await message.answer_photo(photo)
            await message.answer(f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
        except FileNotFoundError:
            await message.answer(f'Ошибка: файл {file_path} не найден.')
        except Exception as e:
            await message.answer(f'Произошла ошибка: {str(e)}')
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_buy)


@dp.callback_query(F.data == 'product_buying')
async def send_confirm_message(callback: CallbackQuery):
    await callback.message.answer('Вы успешно приобрели продукт!')


@dp.message(F.text == 'Информация')
async def main_info(message: Message):
    await message.answer('Мы заботимся о вашем здоровье, даже когда вы о нем забываете')


@dp.message(F.text == 'Регистрация')
async def sing_up(message: Message, state: FSMContext):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await state.set_state(RegistrationState.username)


@dp.message(RegistrationState.username)
async def set_username(message: Message, state: FSMContext):
    if is_included(message.text) is False:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await state.set_state(RegistrationState.email)
    else:
        await message.answer(f'Пользователь "{message.text}" уже существует, введите другое имя')
        await state.set_state(RegistrationState.username)

@dp.message(RegistrationState.email)
async def set_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await state.set_state(RegistrationState.age)


@dp.message(RegistrationState.age)
async def set_age(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    data = await state.get_data()
    add_user(data.get('username'), data.get('email'), data.get('age'))
    await message.answer('Новый пользователь добавлен')
    await state.clear()


@dp.message()
async def handle_unknown_message(message: Message):
    await message.answer('Введите команду /start, чтобы начать общение.')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
