import logging
import os
import aiogram
from dotenv import load_dotenv
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from static import constants
from location import location_parser

# Set up logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

# Set up bot and dispatcher objects
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)

# Defined welcome keyboard
welcome_keyboard = ReplyKeyboardMarkup(
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


# Define the function to send the message with the keyboard
async def send_keyboard(message: types.Message):
    logging.info(f'Пользователю {message.from_user.username} отправлено основное сообщение и показана клавиатура')
    await message.answer(constants.main_message, reply_markup=welcome_keyboard, parse_mode='HTML')


# Define the function to handle button clicks
async def button_click_handler(message: types.Message):
    button_text = message.text
    logging.info(f'User {message.from_user.username} clicked button {button_text}')
    await message.answer(f'You clicked {button_text}')


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
    await message.reply(result, parse_mode='HTML')


# Define the function to handle commands /start and /help
@dp.message_handler(commands=['start', 'help'])
async def send_start_message(message: types.Message):
    logging.info(f'User {message.from_user.username} отправил /start или /help')
    await send_keyboard(message)


# Add handlers to process button clicks
dp.register_message_handler(button_click_handler, Text(equals=['btn1', 'btn2', 'btn3', 'btn4', 'btn5']), state='*')

# Start the bot
if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
