from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
import asyncio
import crud_functions

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Информация')
        ],
        [KeyboardButton(text='Купить')]
    ], resize_keyboard=True
)

catalog_kb = InlineKeyboardMarkup(row_width=4)
button1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
catalog_kb.add(button1, button2, button3, button4)


@dp.message_handler(commands='start')
async def start(message):
    await message.answer(f'Привет! Я бот помогающий Вашему здоровью.\n'
                         f'Чтобы начать, нажмите "Рассчитать"', reply_markup=start_menu)


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer(f'Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f'Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    calories_m = 10 * weight + 6.25 * growth - 5 * age + 5
    calories_w = 10 * weight + 6.25 * growth - 5 * age - 161

    global a
    global g
    global w
    global c_m
    global c_w
    a = age
    g = growth
    w = weight
    c_m = calories_m
    c_w = calories_w
    await message.answer('Расчёт произведён, посмотрите информацию')

    @dp.message_handler(text='Информация')
    async def inform(message):
        await message.answer(f'Ваш возраст:  {a}\nВаш рост:      {g}\nВаш вес:          {w}\n'
                             f'Ваша норма калорий: {c_m}, если вы мужчина\n    '
                             f'                                      {c_w}, если вы женщина')

    await UserState.age.set()

    @dp.message_handler(text='Купить')
    async def get_buying_list(message):
        products = crud_functions.get_all_product()
        for product in products:
            with open(f'images/{product[0]}.png', 'rb') as img:
                await message.answer_photo(img)
            await message.answer(f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
        await message.answer('Выберите продукт для покупки: ', reply_markup=catalog_kb)

    @dp.callback_query_handler(text='product_buying')
    async def send_confirm_message(call):
        await call.message.answer('Вы успешно приобрели продукт!')
        await call.answer()

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
