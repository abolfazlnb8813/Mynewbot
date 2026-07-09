#Start coding bot
#dev : Abolfazl nb
import telebot
import sqlite3
import datetime

bot = telebot.TeleBot("8654313730:AAHTz96pfOyDmsUo0MlmNpMRzGO7eM7bYeQ")

message_textt_userr = None

first_button = telebot.types.InlineKeyboardButton("حساب کاربری", callback_data='first')
support_button = telebot.types.InlineKeyboardButton("پشتیبانی", callback_data='support')
off_support = telebot.types.InlineKeyboardButton("ارتباط مستقیم", url='https://t.me/qpiqu')
buttons_markup = telebot.types.InlineKeyboardMarkup()
buttons_markup.add(first_button, support_button)
buttons_markup.add(off_support)


back_button = telebot.types.InlineKeyboardButton("برگشت", callback_data='back')
back_markup = telebot.types.InlineKeyboardMarkup()
back_markup.add(back_button)


admin_message = telebot.types.InlineKeyboardButton("ارسال پیام به کاربر", callback_data='send_admin')
admin_message_markup = telebot.types.InlineKeyboardMarkup()
admin_message_markup.add(admin_message)


def send_admin_to_user(message):
    global message_textt_userr
    admin_messageeee = message.text
    bot.send_message(message_textt_userr, f"<b>پیام از طرف ادمین انلاین</b>\n{admin_messageeee}", parse_mode='HTML')


def send_user_to_admin(message):
    global message_textt_userr
    user_id = message.chat.id
    message_textt_userr = user_id
    user_message = message.text
    first_name = message.chat.first_name
    user_name = message.chat.username
    admin_id = 8561815342
    userr_data = bot.send_message(admin_id, f"<b>پیام جدید از کاربر {first_name}</b>\n<b>مشخصات پیام کاربر</b>\n<b>{user_message}</b>\n<b>یوسرنیم کاربر</b> : <b>@{user_name}</b>", parse_mode='HTML', reply_markup=admin_message_markup)


@bot.message_handler(commands=['start'])
def start_handler(message):
    now = datetime.datetime.now()
    user_id = message.chat.id
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    user_name = message.chat.username
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, date TEXT, first_name TEXT, last_name TEXT, user_name TEXT)")
    con.commit()
    cur.execute("INSERT OR IGNORE INTO users VALUES(?,?,?,?,?)", (user_id, now, first_name, last_name, user_name))
    con.commit()
    cur.execute("SELECT first_name FROM users WHERE id = ?", (user_id,))
    name = cur.fetchone()
    data = name[0]
    bot.send_chat_action(message.chat.id, action='typing')
    bot.send_message(message.chat.id, f"<b>سلام {data} به ربات Support خوش امدید</b>", reply_markup=buttons_markup, parse_mode='HTML')


    con.close()


@bot.callback_query_handler(func=lambda call: True)
def call_handler(call):
    if call.data == 'first':
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, date TEXT, first_name TEXT, last_name TEXT, user_name TEXT)")
        con.commit()
        user_id = call.message.chat.id
        first_name = call.message.chat.first_name
        last_name = call.message.chat.last_name
        user_name = call.message.chat.username
        cur.execute("SELECT date FROM users WHERE id = ?", (user_id,))
        timee = cur.fetchone()
        data = timee[0]
        bot.edit_message_text(f"<b>سلام کاربر عزیز به بخش حساب کاربری ربات Support  خوش امدید</b>\n<b>اسم شما</b> : {first_name}\n<b>فامیلی شما</b> : {last_name}\n<b>یوزرنیم شما</b> : @{user_name}\n<b>ایدی عددی شما</b> : <code>{user_id}</code>\n<b>تاریخ عضویت شما</b> : {data}\n\n\n;)", call.message.chat.id, call.message.message_id, reply_markup=back_markup, parse_mode='HTML')


    elif call.data == 'support':
        messagee = bot.edit_message_text("<b>به پشتیبانی انلاین وصل شدی</b>\n<i>پیامت رو براش بفرست</i>", call.message.chat.id, call.message.message_id, reply_markup=back_markup, parse_mode='HTML')
        bot.register_next_step_handler(messagee, send_user_to_admin)
        bot.send_message(call.message.chat.id, "<b>پیام با موفقیت ارسال شد</b>", parse_mode='HTML')

    elif call.data == 'send_admin':
        messageee = bot.edit_message_text("به کاربر پیام بفرست", call.message.chat.id, call.message.message_id, reply_markup=back_markup)
        bot.register_next_step_handler(messageee, send_admin_to_user)
        bot.send_message(call.message.chat.id, "<b>پیام با موفقیت ارسال شد</b>", parse_mode='HTML')


    elif call.data == 'back':
        user_id = call.message.chat.id
        first_name = call.message.chat.first_name
        last_name = call.message.chat.last_name
        user_name = call.message.chat.username
        now = datetime.datetime.now()
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, date TEXT, first_name TEXT, last_name TEXT, user_name TEXT)")
        con.commit()
        cur.execute("SELECT first_name FROM users WHERE id = ?", (user_id,))
        name = cur.fetchone()
        data = name[0]
        bot.edit_message_text(f"<b>سلام {data} به ربات Support خوش امدید</b>",call.message.chat.id, call.message.message_id, reply_markup=buttons_markup, parse_mode='HTML')

bot.infinity_polling()
#End coding