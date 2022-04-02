from decimal import Decimal
from gettext import find
import re
import string
from turtle import title
from unicodedata import decimal
from urllib import request
import datetime
import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType, Poll
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from bs4 import BeautifulSoup

updater = Updater(token="5282110317:AAGKwev1D3gJMJIwFQ3bly5KjAM4-DaNoCM")
dispetcher = updater.dispatcher

MENU = ReplyKeyboardMarkup([
    [KeyboardButton(text = "👨‍👨‍👧‍👦 user haqida ma'lumot olish")],
    [KeyboardButton(text = "🌤 ob - havo ma'lumotlari")],
    [KeyboardButton(text = "💵 valyuta kursini bilish")]
], resize_keyboard = True)

BUTTONS_USER = ReplyKeyboardMarkup([
    [KeyboardButton(text = '🆔 user id ni bilish'), KeyboardButton(text = 'ℹ️ username ni bilish')],
    [KeyboardButton(text = '🔤 ismni bilish'), KeyboardButton(text = '🔤 familiyani bilish')],
    [
      KeyboardButton(text = '❓ savolnoma yasash', request_poll=KeyboardButtonPollType(type=Poll.QUIZ)),
      KeyboardButton(text = '🔍 viktorina yasash', request_poll=KeyboardButtonPollType(type=Poll.REGULAR))
    ],
    [KeyboardButton(text = "🔙 orqaga")]
], resize_keyboard = True)

BUTTONS_HAVO = ReplyKeyboardMarkup([
    [KeyboardButton('🌤 Toshkent'), KeyboardButton('🌤 Namangan'), KeyboardButton('🌤 Andijon')],
    [KeyboardButton('🌤 Farg\'ona'), KeyboardButton('🌤 Sirdaryo'), KeyboardButton('🌤 Qashqadaryo')],
    [KeyboardButton('🌤 Buxoro'), KeyboardButton('🌤 Samarqand'), KeyboardButton('🌤 Jizzax')],
    [KeyboardButton('🌤 Xorazm'), KeyboardButton('🌤 Qoraqalpoq'), KeyboardButton('🌤 Navoiy')],
    [KeyboardButton(text = "🔙 orqaga")]
], resize_keyboard = True)

# Kiritilgan sonlarni harfda chiqarish
def birlar(value):
    birlar = {
        1 : 'bir',
        2 : 'ikki',
        3 : 'uch',
        4 : "to'rt",
        5 : 'besh',
        6 : 'olti',
        7 : 'yetti',
        8 : 'sakkiz',
        9 : "to'qqiz"
    }
    natija = birlar.get(value, '')
    return natija

def onlar(value):
    onlar = {
        1 : "o'n ",
        2 : "yigirma ",
        3 : "o'ttiz ",
        4 : 'qirq ',
        5 : 'ellik ',
        6 : 'oltmish ',
        7 : 'yetmish ',
        8 : 'sakson ',
        9 : "to'qson "
    }
    natija = onlar.get(value, '')
    return natija

def yuzlar_xonasi(number):
    if len(str(number)) == 1:
        return birlar(number)
    elif len(str(number)) == 2:
        bir = number % 10
        on = number // 10
        onlik = onlar(on) + birlar(bir)
        return onlik
    else:
        v = number % 100
        bir = v % 10
        on = v // 10
        yuz = number // 100
        yuzlik = birlar(yuz) + ' yuz ' + onlar(on) + birlar(bir)
        return yuzlik

def minglar_xonasi(number):
    if number != 0:
        if len(str(number)) == 1:
            birlik = birlar(number) + ' ming '
            return birlik
        elif len(str(number)) == 2:
            bir = number % 10
            on = number // 10
            onlik = onlar(on) + birlar(bir) + ' ming '
            return onlik
        else:
            v = number % 100
            bir = v % 10
            on = v // 10
            yuz = number // 100
            yuzlik = birlar(yuz) + ' yuz ' + onlar(on) + birlar(bir) + ' ming '
            return yuzlik
    else:
        return ''

def millionlar_xonasi(number):
    if number != 0:
        if len(str(number)) == 1:
            birlik = birlar(number) + ' million '
            return birlik
        elif len(str(number)) == 2:
            bir = number % 10
            on = number // 10
            onlik = onlar(on) + birlar(bir) + ' million '
            return onlik
        else:
            v = number % 100
            bir = v % 10
            on = v // 10
            yuz = number // 100
            yuzlik = birlar(yuz) + ' yuz ' + onlar(on) + birlar(bir) + ' million '
            return yuzlik
    else:
        return ''

def milliardlar_xonasi(number):
    if number != 0:
        if len(str(number)) == 1:
            birlik = birlar(number) + ' milliard '
            return birlik
        elif len(str(number)) == 2:
            bir = number % 10
            on = number // 10
            onlik = onlar(on) + birlar(bir) + ' milliard '
            return onlik
        else:
            v = number % 100
            bir = v % 10
            on = v // 10
            yuz = number // 100
            yuzlik = birlar(yuz) + ' yuz ' + onlar(on) + birlar(bir) + ' milliard '
            return yuzlik
    else:
        return ''

def trillionlar_xonasi(number):
    if number != 0:
        if len(str(number)) == 1:
            birlik = birlar(number) + ' trillion '
            return birlik
        elif len(str(number)) == 2:
            bir = number % 10
            on = number // 10
            onlik = onlar(on) + birlar(bir) + ' trillion '
            return onlik
        else:
            v = number % 100
            bir = v % 10
            on = v // 10
            yuz = number // 100
            yuzlik = birlar(yuz) + ' yuz ' + onlar(on) + birlar(bir) + ' trillion '
            return yuzlik
    else:
        return ''
# Kiritilgan sonlarni harfda chiqarish

def start_handler(update, context):
    update.message.reply_text(text = "Assalomu aleykum!!! Botga xush kelibsiz! 🎉", reply_markup = MENU)

def orqaga_handler(update, contaxt):
    update.message.reply_text(text = "📋 Menu", reply_markup = MENU)

def buttons_user_handler(update: Update, context: CallbackContext):
    update.message.reply_text(text="O'zingizni akkauntingiz haqida ma'lumot olish. 👇", reply_markup=BUTTONS_USER)

def buttons_havo_handler(update, context):
    update.message.reply_text(text = "Ob - havo bo'yicha ma'lumot olish. 👇", reply_markup = BUTTONS_HAVO)

def text_handler(update, context):
    xabar = update.message.text
    user = update.message.from_user
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")
    if xabar.isdigit() == True:
        xabar = int(xabar)
        if xabar < 0:
            javob = "Siz 0 dan kichik son kiritdingiz"
            update.message.reply_text(text = f"Hurmatli <b>{user.first_name}</b> siz yuborgan son: <b>{javob}</b> vaqti: <b>{date}</b>", parse_mode = "HTML")
        elif xabar == 0:
            javob = "Nol"
            update.message.reply_text(text = f"Hurmatli <b>{user.first_name}</b> siz yuborgan son: <b>{javob}</b> vaqti: <b>{date}</b>", parse_mode = "HTML")
        elif 1 <= len(str(xabar)) and len(str(xabar)) <= 3:
            javob = yuzlar_xonasi(xabar)
            update.message.reply_text(text = f"Hurmatli <b>{user.first_name}</b> siz yuborgan son: <b>{javob}</b> vaqti: <b>{date}</b>", parse_mode = "HTML")
        elif 4 <= len(str(xabar)) and len(str(xabar)) <= 6:
            yuz = xabar % 1000
            ming = xabar // 1000
            javob = minglar_xonasi(ming) + yuzlar_xonasi(yuz)
            update.message.reply_text(text = f"Hurmatli <b>{user.first_name}</b> siz yuborgan son: <b>{javob}</b> vaqti: <b>{date}</b>", parse_mode = "HTML")
        elif 7 <= len(str(xabar)) and len(str(xabar)) <= 9:
            v = xabar % 1000000
            yuz = v % 1000
            ming = v // 1000
            million = xabar // 1000000
            javob = millionlar_xonasi(million) + minglar_xonasi(ming) + yuzlar_xonasi(yuz)
            update.message.reply_text(text = f"Hurmatli <b>{user.first_name}</b> siz yuborgan son: <b>{javob}</b> vaqti: <b>{date}</b>", parse_mode = "HTML")
        elif 10 <= len(str(xabar)) and len(str(xabar)) <= 12:
            v = xabar % 1000000000 # millionlar qoldi
            v2 = v % 1000000        # minglar qoldi
            yuz = v2 % 1000
            ming = v2 // 1000
            million = v // 1000000
            milliard = xabar // 1000000000
            javob = milliardlar_xonasi(milliard) + millionlar_xonasi(million) + minglar_xonasi(ming) + yuzlar_xonasi(yuz)
            update.message.reply_text(text = f"Hurmatli <b>{user.first_name}</b> siz yuborgan son: <b>{javob}</b> vaqti: <b>{date}</b>", parse_mode = "HTML")
        elif 13 <= len(str(xabar)) and len(str(xabar)) <= 15:
            v = xabar % 1000000000000 # milliardlar qoldi
            v2 = v % 1000000000        # millionlar qoldi
            v3 = v2 % 1000000          # minglar qoldi
            yuz = v3 % 1000
            ming = v3 // 1000
            million = v2 // 1000000
            milliard = v // 1000000000
            trillion = xabar // 1000000000000
            javob = trillionlar_xonasi(trillion) + milliardlar_xonasi(milliard) + millionlar_xonasi(million) + minglar_xonasi(ming) + yuzlar_xonasi(yuz)
            update.message.reply_text(text = f"Hurmatli <b>{user.first_name}</b> siz yuborgan son: <b>{javob}</b> vaqti: <b>{date}</b>", parse_mode = "HTML")
        else:
            javob = """Siz dasturda belgilangan chegaradan o'tdingiz. Sizga undan keyingi sonlarni harf ko'rinishida chiqarish kerak bo'lsa, 91 357-04-05 ga murojaat qiling!"""
            update.message.reply_text(text = f"Hurmatli <b>{user.first_name}</b> siz yuborgan son: <b>{javob}</b> vaqti: <b>{date}</b>", parse_mode = "HTML")
    else:           
        update.message.reply_text(text = f"Hurmatli <b>{user.first_name}</b> siz yuborgan xabar: <b>{xabar}</b> vaqti: <b>{date}</b>", parse_mode = "HTML")

def id_handler(update, context):
    user = update.message.from_user
    update.message.reply_text(text = f"Hurmatli <b>{user.first_name}</b> sizning id: <b>{user.id}</b>", parse_mode = "HTML")

def username_handler(update, context):
    user = update.message.from_user
    update.message.reply_text(text = f"Hurmatli <b>{user.first_name}</b> sizning username: <b>{user.username}</b>", parse_mode = "HTML")

def first_name_handler(update, context):
    user = update.message.from_user
    update.message.reply_text(text = f"Sizning ismingiz: <b>{user.first_name}</b>", parse_mode = "HTML")

def last_name_handler(update, context):
    user = update.message.from_user
    update.message.reply_text(text = f"Hurmatli <b>{user.first_name}</b> sizning familiyangiz: <b>{user.last_name}</b>", parse_mode = "HTML")

def valyuta_handler(update, context):
    request = requests.get("https://hamkorbank.uz/uz/").text
    soup = BeautifulSoup(request, "html.parser")
    soup_span1 = soup.find('span', class_='key', string='Sotib olish')
    olish = soup_span1.find_next_sibling('span', class_='val').string.strip()
    soup_span2 = soup.find('span', class_='key', string='Sotish')
    sotish = soup_span2.find_next_sibling('span', class_='val').string.strip()
    update.message.reply_text(text = f"<b>Bugungi dollar kursi(USD)\n</b><b>Sotib olish: </b>{olish}\n<b>Sotish: </b>{sotish}", parse_mode = "HTML")

def namangan_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/namangan").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>🌤 Namangan bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")
    
def toshkent_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/tashkent").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>🌤 Toshkent bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def andijon_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/andijan").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>🌤 Andijon bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def fergana_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/ferghana").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>🌤 Farg\'ona bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def sirdaryo_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/gulistan").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>🌤 Sirdaryo bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def qashqadaryo_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/karshi").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>🌤 Qashqadaryo bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def buxoro_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/bukhara").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>🌤 Buxoro bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def samarqand_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/samarkand").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>🌤 Samarqand bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def jizzax_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/jizzakh").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>🌤 Jizzax bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def xorazm_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/urgench").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>🌤 Xorazm bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def qoraqalpoq_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/nukus").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>🌤 Qoraqalpoq bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def navoiy_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/navoi").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>🌤 Navoiy bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")


dispetcher.add_handler(CommandHandler("start", callback=start_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("👨‍👨‍👧‍👦 user haqida ma'lumot olish"), callback=buttons_user_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🌤 ob - havo ma'lumotlari"), callback=buttons_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🆔 user id ni bilish"), callback=id_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("ℹ️ username ni bilish"), callback=username_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🔤 ismni bilish"), callback=first_name_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🔤 familiyani bilish"), callback=last_name_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🔙 orqaga"), callback=orqaga_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("💵 valyuta kursini bilish"), callback=valyuta_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🌤 Namangan"), callback=namangan_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🌤 Toshkent"), callback=toshkent_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🌤 Andijon"), callback=andijon_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🌤 Farg\'ona"), callback=fergana_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🌤 Sirdaryo"), callback=sirdaryo_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🌤 Qashqadaryo"), callback=qashqadaryo_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🌤 Buxoro"), callback=buxoro_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🌤 Samarqand"), callback=samarqand_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🌤 Jizzax"), callback=jizzax_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🌤 Xorazm"), callback=xorazm_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🌤 Qoraqalpoq"), callback=qoraqalpoq_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("🌤 Navoiy"), callback=navoiy_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text, callback=text_handler))

updater.start_polling()
updater.idle()