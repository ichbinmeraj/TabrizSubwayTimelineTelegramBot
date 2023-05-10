import os
import json
import telebot
import pytz
from datetime import datetime, time
from telebot import types
from keep_alive import keep_alive

with open('timeline.json', 'r') as file:
  data = json.load(file)


# Create a new bot instance with your API token obtained from BotFather
BotToken = os.environ['BotToken']
bot = telebot.TeleBot(BotToken)

# Set the timezone to Iran timezone
ir_tz = pytz.timezone('Asia/Tehran')


@bot.message_handler(commands=['start'])
def send_welcome(message):
  keyboard = types.InlineKeyboardMarkup()
  b1 = types.InlineKeyboardButton(text='به سمت میدان کهن', callback_data='d_0')
  b2 = types.InlineKeyboardButton(text='به سمت ائل‌گولی', callback_data='d_1')

  keyboard.row(b1, b2)
  
  bot.reply_to(message, 'مسیر مترو خود را انتخاب کنید.', reply_markup=keyboard)
   
  uid = str(message.from_user.id)
  with open('user_id_name.json', 'r+' ) as f:
    users = json.load(f)
    if uid in users:
      pass
    else:  
      firstname = message.from_user.first_name
      username = message.from_user.username
      users.update({f"{uid}": f"{firstname}-{username}"})
      f.seek(0)
      json.dump(users, f, indent = 2)
    

# Handle button presses
@bot.callback_query_handler(func=lambda call: call.data.startswith('d_'))
def handle_d_callback_query(call):
  
  s_d = call.data.split("_")[1]
  c1 = f's_0_{s_d}'
  c2 = f's_1_{s_d}'
  c3 = f's_2_{s_d}'
  c4 = f's_3_{s_d}'
  c5 = f's_4_{s_d}'
  c6 = f's_5_{s_d}'
  c7 = f's_6_{s_d}'
  c8 = f's_7_{s_d}'
  c9 = f's_8_{s_d}'
  c10 = f's_9_{s_d}'
  c11 = f's_10_{s_d}'
  c12 = f's_11_{s_d}'
  
  # Create a custom keyboard with an inline button
  keyboard = types.InlineKeyboardMarkup()
  s1 = types.InlineKeyboardButton(text='ائل‌گولی', callback_data=c1)
  s2 = types.InlineKeyboardButton(text='سهند', callback_data=c2)
  s3 = types.InlineKeyboardButton(text='امام رضا', callback_data=c3)
  s4 = types.InlineKeyboardButton(text='خیلم', callback_data=c4)
  s5 = types.InlineKeyboardButton(text='29 بهمن', callback_data=c5)
  s6 = types.InlineKeyboardButton(text='استاد شهریار', callback_data=c6)
  s7 = types.InlineKeyboardButton(text='دانشگاه', callback_data=c7)
  s8 = types.InlineKeyboardButton(text='آبرسان', callback_data=c8)
  s9 = types.InlineKeyboardButton(text='قطب', callback_data=c9)
  s10 = types.InlineKeyboardButton(text='شهید بهشتی', callback_data=c10)
  s11 = types.InlineKeyboardButton(text='میدان ساعت', callback_data=c11)
  s12 = types.InlineKeyboardButton(text='میدان کهن', callback_data=c12)
  
  keyboard.row(s3, s2, s1)
  keyboard.row(s6, s5, s4)
  keyboard.row(s9, s8, s7)
  keyboard.row(s12, s11, s10)
  
  message = call.message
  bot.reply_to(message, 'ایستگاه خود را انتخاب کنید.', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('s_'))
def handle_s_callback_query(call):

  message = call.message
  s = int(call.data.split("_")[1])
  d = int(call.data.split("_")[2])

 
  first_d = data["destinations"][d]
  station =  first_d["stations"][s]
  user_id = call.from_user.id
  user_name = call.from_user.first_name
  username = call.from_user.username
  bot.send_message(chat_id="-1001908601017", text=f"{user_id}-{user_name}/d:{d}-s:{s}-@{username}")

  # Get the current time in Iran timezone
  now = datetime.now(ir_tz).time()
  time_str = now.strftime('%H:%M')
  weekday_str = now.strftime('%A')

  if weekday_str == "friday":
    station_friday = station["friday"]["times"]
    next_departures = []
    
    for time_str in station_friday:
      time_obj = datetime.strptime(time_str, "%H:%M").time()
      if time(time_obj.hour, time_obj.minute) >= now and len(next_departures) < 3:
        next_departures.append(time_str)

    
    first_departure = next_departures[0]
    secound_departure = next_departures[1]
    third_departure = next_departures[2]
    bot.reply_to(message, f''' 
    نزدیک ترین تایمی که مترو در ایستگاه خواهد بود : {first_departure}
تایم های متوالی بعدی : {secound_departure}, {third_departure}
    ''')
    
  else :
    station_weekday = station["weekday"]["times"]
    next_departures = []
    
    
    for time_str in station_weekday:
      time_obj = datetime.strptime(time_str, "%H:%M").time()
      if time(time_obj.hour, time_obj.minute) >= now and len(next_departures) < 3:
        next_departures.append(time_str)
        
    first_departure = next_departures[0]
    secound_departure = next_departures[1]
    third_departure = next_departures[2]
    bot.reply_to(message, f''' 
    نزدیک ترین تایمی که مترو در ایستگاه خواهد بود : {first_departure}
تایم های متوالی بعدی : {secound_departure}, {third_departure}
    ''')


@bot.message_handler(commands=['contact'])
def send_admin_info(message):
  bot.reply_to(message, f''' برای پیشنهادات و انتقادات : https://t.me/merajsafari
    ''')
keep_alive()
bot.polling()
