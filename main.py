import json
import telebot
import pytz
from datetime import datetime, time
from telebot import types
from keep_alive import keep_alive

data = None
userData = None
with open("timeline.json", "r") as f:
    data = json.load(f)

# Create a new bot instance with your API token obtained from BotFather
BotToken = "BotToken"
bot = telebot.TeleBot(BotToken)

# Set the timezone to Iran timezone
ir_tz = pytz.timezone("Asia/Tehran")

welcomeKeyboard = types.InlineKeyboardMarkup()
messages = ["به سمت ایستگاه ائل‌گولی", "به سمت ایستگاه نور"]
for i in range(len(messages)):
    welcomeKeyboard.row(
        types.InlineKeyboardButton(text=messages[i], callback_data=f"d_{i}")
    )


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "مسیر مترو خود را انتخاب کنید.", reply_markup=welcomeKeyboard)

    uid = str(message.from_user.id)
    userDataF(uid, message.from_user.first_name, message.from_user.username)


c = [
    "ائل‌گولی",
    "سهند",
    "امام رضا",
    "خیام",
    "29 بهمن",
    "استاد شهریار",
    "دانشگاه",
    "آبرسان",
    "قطب",
    "شهید بهشتی",
    "میدان ساعت",
    "میدان کهن",
    "قونقا",
    "گازران",
    "لاله",
    "امام حسین",
    "شهید باکری",
    "نور",
]


# Handle button presses
@bot.callback_query_handler(func=lambda call: call.data.startswith("d_"))
def handle_d_callback_query(call):
    s_d = call.data.split("_")[1]
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(c) // 3):
        keyboard.row(
            types.InlineKeyboardButton(text=c[i * 3], callback_data=f"s_{i*3}_{s_d}"),
            types.InlineKeyboardButton(
                text=c[(i * 3) + 1], callback_data=f"s_{(i*3)+1}_{s_d}"
            ),
            types.InlineKeyboardButton(
                text=c[(i * 3) + 2], callback_data=f"s_{(i*3)+2}_{s_d}"
            ),
        )

    message = call.message
    bot.reply_to(message, "ایستگاه خود را انتخاب کنید.", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("s_"))
def handle_s_callback_query(call):
    global data
    twoDest = False
    message = call.message
    s = int(call.data.split("_")[1])
    d = int(call.data.split("_")[2])
    # second_d = data["destinations"][0]
    second_d = None
    station2 = None
    #11 Meydankohan
    if d == 0 and (12 <= s <= 17):
        twoDest = True
        station2 = data["destinations"][1]["stations"][11]
        second_d = data["destinations"][1]
    elif d == 1 and (0 <= s <= 10):
        twoDest = True
        station2 = data["destinations"][2]["stations"][0]
        second_d = data["destinations"][0] 
    if d == 0:
        first_d = data["destinations"][1]
    if d == 1:
        first_d = data["destinations"][2]
    
    if twoDest:
        m = s
        if d == 0:
            m = m-11
        station = second_d["stations"][m]
    else:
        m = s
        if d == 1:
            m = m-11
        station = first_d["stations"][m]


   

    # Get the current time in Iran timezone
    now = datetime.now(ir_tz).time()
    time_str = now.strftime("%H:%M")
    weekday_str = now.strftime("%A")
    print(station2)
    print(station)
    
    if weekday_str == "friday":
        station = station["friday"]["times"]
        if twoDest:
            station2 = station2["friday"]["times"]
    else:
        station = station["weekday"]["times"]
        if twoDest:
            station2 = station2["weekday"]["times"]
    
    next_departures = []
    next_departures2 = []

    for time_str in station:
        time_obj = datetime.strptime(time_str, "%H:%M").time()
        if time(time_obj.hour, time_obj.minute) >= now and len(next_departures) < 3:
            next_departures.append(time_str)
    if twoDest:
        for time_str in station2:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            if time(time_obj.hour, time_obj.minute) >= now and len(next_departures2) < 3:
                next_departures2.append(time_str)
    times2 = None
    if twoDest:
        if len(next_departures2) > 2:
            first_departure = next_departures2[0]
            secound_departure = next_departures2[1]
            third_departure = next_departures2[2]
            times2 = f"""
            
توجه!
برای ادامه سفر خود باید در ایستگاه میدان کهن پیاده شده و مترو خود عوض کنید.
نزدیک ترین تایمی که مترو در این ایستگاه خواهد بود : {first_departure}
    تایم های متوالی بعدی : {secound_departure}, {third_departure}
        """
        elif len(next_departures2) == 2:
            first_departure = next_departures2[0]
            secound_departure = next_departures2[1]
            times2 = f"""
            
توجه!
برای ادامه سفر خود باید در ایستگاه میدان کهن پیاده شده و مترو خود عوض کنید.
نزدیک ترین تایمی که مترو در این ایستگاه خواهد بود : {first_departure}
    آخرین مترو در این ایستگاه : {secound_departure}
        """

        elif len(next_departures2) == 1:
            first_departure = next_departures2[0]
            times2 = f"""
            
توجه!
برای ادامه سفر خود باید در ایستگاه میدان کهن پیاده شده و مترو خود عوض کنید.
نزدیک ترین تایمی که مترو در این ایستگاه خواهد بود-این آخرین مترو می باشد : {first_departure}
        """

        elif len(next_departures2) == 0:
            times2 = f""" 
        متاسفانه هم اکنون مترو تعطیل هست
        
            تایم کاری مترو تبریز:
    روز های هفته - از 06:26 الی 21:30
    روز های جمعه - از 11:30 الی 14:34

        """


    if len(next_departures) > 2:
        first_departure = next_departures[0]
        secound_departure = next_departures[1]
        third_departure = next_departures[2]
        times = f"""
    نزدیک ترین تایمی که مترو در این ایستگاه خواهد بود : {first_departure}
تایم های متوالی بعدی : {secound_departure}, {third_departure}
    """
        if twoDest:
            times += times2
        bot.reply_to(message,times)
    elif len(next_departures) == 2:
        first_departure = next_departures[0]
        secound_departure = next_departures[1]
        times = f""" 
    نزدیک ترین تایمی که مترو در این ایستگاه خواهد بود : {first_departure}
آخرین مترو در این ایستگاه : {secound_departure}
    """
        if twoDest:
            times += times2
        bot.reply_to(
            message,
            times
        )
    elif len(next_departures) == 1:
        first_departure = next_departures[0]
        times = f""" 
    نزدیک ترین تایمی که مترو در این ایستگاه خواهد بود-این آخرین مترو می باشد : {first_departure}
    """
        if twoDest:
            times += times2
        bot.reply_to(
            message,
            times
        )

    elif len(next_departures) == 0:
        times = f""" 
    متاسفانه هم اکنون مترو تعطیل هست
    
        تایم کاری مترو تبریز:
روز های هفته - از 06:26 الی 21:30
روز های جمعه - از 11:30 الی 14:34

    """
        if twoDest:
            times += times2
        bot.reply_to(
            message,
            times
        )


@bot.message_handler(commands=["contact"])
def send_admin_info(message):
    bot.reply_to(
        message,
        f""" برای پیشنهادات و انتقادات :
  https://t.me/unknownMs_Bot?start=GfB-586430089-pwuWPJ
    """,
    )


@bot.message_handler(commands=["about"])
def send_admin_info(message):
    bot.reply_to(
        message,
        f""" با استفاده از این ربات میتوانید بفهمید که نزدیک ترین مترو در چه ساعتی در ایستگاه مورد نظر خواهد بود و برنامه زمانی خود را با آن تایم هماهنگ کنید.

تایم کاری مترو تبریز:
روز های هفته - از 06:26 الی 21:30
روز های جمعه - از 11:30 الی 14:34

it's late :)
    """,
    )


keep_alive()
bot.polling()
