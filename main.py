import telebot
import pytz
from datetime import datetime
from telebot import types

# Create a new bot instance with your API token obtained from BotFather
bot = telebot.TeleBot('YOUR_API_TOKEN')

# Set the timezone to Iran timezone
ir_tz = pytz.timezone('Asia/Tehran')

# Handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Create a custom keyboard with an inline button
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text='Get Time', callback_data='get_time')
    keyboard.add(callback_button)

    # Send the message with the custom keyboard
    bot.reply_to(message, 'Hello! Press the button below to get the current time in Iran:', reply_markup=keyboard)

# Handle button presses
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == 'get_time':
        # Get the current time in Iran timezone
        now = datetime.now(ir_tz)
        time_str = now.strftime('%H:%M:%S')
        weekday_str = now.strftime('%A')

        # Send the formatted time and weekday strings as a reply to the button press
        bot.answer_callback_query(callback_query_id=call.id, text=f"The current time is {time_str} on a {weekday_str} in Iran.")

# Start the bot and keep it running
bot.polling()
