import logging
import os
import aiogram
from static import constants
from dotenv import load_dotenv
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
    await message.answer(constants.main_message, reply_markup=welcome_keyboard)


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
    await message.reply(f"Your coordinates are: {latitude}, {longitude}")


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
