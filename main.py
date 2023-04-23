import logging
import os
import aiogram
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
            KeyboardButton(text="btn1"),
            KeyboardButton(text="btn2"),
            KeyboardButton(text="btn3"),
        ],
        [
            KeyboardButton(text="btn4"),
            KeyboardButton(text="btn5"),
        ]
    ],
    resize_keyboard=True
)


# Define the function to send the message with the keyboard
async def send_keyboard(message: types.Message):
    logging.info("текст отправлен")
    await message.answer("Choose a button:", reply_markup=welcome_keyboard)


# Define the function to handle button clicks
async def button_click_handler(message: types.Message):
    button_text = message.text
    logging.info(f'User {message.from_user.username} clicked button {button_text}')
    await message.answer(f'You clicked {button_text}')


# Define the function to handle commands /start and /help
@dp.message_handler(commands=['start', 'help'])
async def send_start_message(message: types.Message):
    logging.info(f'User {message.from_user.username} user command {message.text}')
    await send_keyboard(message)


# Add handlers to process button clicks
dp.register_message_handler(button_click_handler, Text(equals=['btn1', 'btn2', 'btn3', 'btn4', 'btn5']), state='*')

# Start the bot
if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
