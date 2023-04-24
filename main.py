import logging
import os
import aiogram
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from static import constants
from location import location_parser
from database.database_scripts import update_state, get_type_and_budget

# Set up logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

# Set up bot and dispatcher objects
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)

# Defined keyboard with button to share location
location_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Я здесь 📍", request_location=True)  # ,
        ]
    ],
    resize_keyboard=True
)

# Defined keyboard with buttons to choose type of establishment
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

# Defined keyboard with buttons to set up budget
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

# Defined keyboard with button to use bot again
try_again_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Попробовать еще')
        ]
    ],
    resize_keyboard=True
)


# Function to send keyboard with budget options
async def send_budget_keyboard(message: types.Message):
    await message.answer(constants.choose_budget, reply_markup=budget_keyboard, parse_mode='HTML')


# Function to send keyboard with button to share location
async def send_location_keyboard(message: types.Message):
    await message.answer(constants.location_message, reply_markup=location_keyboard, parse_mode='HTML')


# Function to handle event when user clicked try again button
async def handle_try_again_button_click(message: types.Message):
    await message.answer(constants.welcome_message, reply_markup=type_keyboard, parse_mode='HTML')


# Function to handle event when user clicked one of the buttons to set up budget
async def handle_budget_button_click(message: types.Message):
    id = message.from_user.id
    text = message.text
    update_state(user_id=id, budget=text)
    await send_location_keyboard(message)


# Function to handle event when user clicked one of the buttons to set up type of establishment
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

    type, budget = get_type_and_budget(message.from_user.id)  # extract data from database

    options = await location_parser.parse_location(latitude, longitude, type, budget)
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


# Register handlers
dp.register_message_handler(handle_type_button_click, lambda message: message.text in ['Бары', 'Кафе', 'Рестораны'])
dp.register_message_handler(handle_budget_button_click, lambda message: message.text in ['Low', 'Medium', 'High'])
dp.register_message_handler(handle_try_again_button_click, lambda message: message.text == 'Попробовать еще')

# Start the bot
if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
