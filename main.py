import logging
import os
import aiogram
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Update
from static import constants
from location import location_parser
from database.database_scripts import update_state

# Set up logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

# Set up bot and dispatcher objects
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)

# Defined welcome keyboard
location_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Я здесь 📍", request_location=True)  # ,
            # KeyboardButton(text="btn2"),
            # KeyboardButton(text="btn3"),
        ]  # ,
        # [
        # KeyboardButton(text="btn4"),
        # KeyboardButton(text="btn5"),
        # ]
    ],
    resize_keyboard=True
)

type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Бары'),
            KeyboardButton(text='Кафе'),
            KeyboardButton(text='Рестораны')
        ]
    ],
    resize_keyboard=True
)

budget_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Low'),
            KeyboardButton(text='Medium'),
            KeyboardButton(text='High')
        ]
    ],
    resize_keyboard=True
)

try_again_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Попробовать еще')
        ]
    ],
    resize_keyboard=True
)


async def send_budget_keyboard(message: types.Message):
    await message.answer(constants.choose_budget, reply_markup=budget_keyboard, parse_mode='HTML')


async def send_location_keyboard(message: types.Message):
    await message.answer(constants.location_message, reply_markup=location_keyboard, parse_mode='HTML')


async def handle_try_again_button_click(message: types.Message):
    await message.answer(constants.welcome_message, reply_markup=type_keyboard, parse_mode='HTML')


async def handle_budget_button_click(message: types.Message):
    id = message.from_user.id
    text = message.text
    update_state(user_id=id, budget=text)
    await send_location_keyboard(message)


async def handle_type_button_click(message: types.Message):
    id = message.from_user.id
    text = message.text
    update_state(user_id=id, type=text)
    await send_budget_keyboard(message)


# Define the function to send the message with the keyboard
async def send_welcome_keyboard(message: types.Message):
    logging.info(f'Пользователю {message.from_user.username} отправлено основное сообщение и показана клавиатура')
    await message.answer(constants.welcome_message, reply_markup=type_keyboard, parse_mode='HTML')


# Handler for handling location messages
@dp.message_handler(content_types=types.ContentType.LOCATION)
async def handle_location(message: types.Message):
    # Extracting latitude and longitude from the message
    latitude = message.location.latitude
    longitude = message.location.longitude

    # Sending the coordinates back to the user
    # price сделать как надо и тип заведения тоже
    options = await location_parser.parse_location(latitude, longitude, 1500)
    sorted_by_distance = dict(sorted(options.items(), key=lambda x: x[1]['distance']))
    result = '<b>Вот, что мне удалось найти:</b>\n\n'
    for key, value in sorted_by_distance.items():
        name = value['name']
        address = value['address']
        phone = value['phone']
        distance = value['distance']
        # if the place not far then 1500 metres, it fits
        if distance <= 1500:
            result += f'<b>{name}</b>\n📍{address}\n📞{phone}\n🚶🏻Находится на расстоянии <b>{int(distance)}м.</b>\n\n'
    await message.answer(result, parse_mode='HTML')
    await message.answer(constants.try_again, reply_markup=try_again_keyboard, parse_mode='HTML')


# Define the function to handle commands /start and /help
@dp.message_handler(commands=['start', 'help'])
async def send_start_message(message: types.Message):
    logging.info(f'User {message.from_user.username} отправил /start или /help')
    await send_welcome_keyboard(message)


dp.register_message_handler(handle_type_button_click, lambda message: message.text in ['Бары', 'Кафе', 'Рестораны'])
dp.register_message_handler(handle_budget_button_click, lambda message: message.text in ['Low', 'Medium', 'High'])
dp.register_message_handler(handle_try_again_button_click, lambda message: message.text == 'Попробовать еще')

# Start the bot
if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
