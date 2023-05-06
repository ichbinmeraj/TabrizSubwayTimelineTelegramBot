# import json

# with open('timings.json', 'r') as file:
#     data = json.load(file)

# for i in range(2):

#     #destination filter
#     first_d = data["destinations"][i]

#     #station filter
#     station =  first_d["stations"][0]

#     #weekday filter
#     station_weekday = station["weekday"]

#     #timing filter
#     station_weekday_times = station_weekday["times"]
    
# print(data["destinations"])
# print(station)
# print(station_weekday)


import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

updater = Updater(token='5988959877:AAEfoolGDMBv9zjWjU0eEUCMu-tmi1S37Xk', use_context=True)

def start(update, context):
    update.message.reply_text('Click the button below to get the current time')
    
    # create a new keyboard with a single button
    keyboard = [[telegram.InlineKeyboardButton("به سمت میدان کهن", callback_data='0'),
        telegram.InlineKeyboardButton("به سمت ائل‌گولی", callback_data='1'),]]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    
    # send the keyboard to the user
    update.message.reply_text('لاین مترو خود را انتخاب کنید', reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query
    if query.data == 'time':
        current_time = query.time
        query.answer(f"Current time is {current_time}")
        
start_handler = CommandHandler('start', start)
button_handler = CallbackQueryHandler(button)

updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(button_handler)

updater.start_polling()
