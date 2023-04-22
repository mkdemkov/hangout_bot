import logging
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up your bot and dispatcher objects
bot = Bot(token='6250730357:AAGMdL7DHHta7WELb792S3YbcWTuza40rAE')
dp = Dispatcher(bot)

# Define your keyboard
keyboard = ReplyKeyboardMarkup(
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
    await message.answer("Choose a button:", reply_markup=keyboard)


# Define the function to handle button clicks
async def button_click_handler(callback_query: types.CallbackQuery):
    logging.info("ХЕНДЛЕР СЛОВИЛ")
    button_text = callback_query.data
    logging.info(button_text)
    await bot.answer_callback_query(callback_query.id, text=f"You clicked {button_text}")


@dp.message_handler(commands=['start', 'help'])
async def send_start_message(message: types.Message):
    logging.info("start clicked")
    await send_keyboard(message)


# Add handlers for your bot
dp.register_callback_query_handler(button_click_handler)

# Start the bot
if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
