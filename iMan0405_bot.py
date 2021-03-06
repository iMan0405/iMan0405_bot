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
    [KeyboardButton(text = "๐จโ๐จโ๐งโ๐ฆ user haqida ma'lumot olish")],
    [KeyboardButton(text = "๐ค ob - havo ma'lumotlari")],
    [KeyboardButton(text = "๐ต valyuta kursini bilish")]
], resize_keyboard = True)

BUTTONS_USER = ReplyKeyboardMarkup([
    [KeyboardButton(text = '๐ user id ni bilish'), KeyboardButton(text = 'โน๏ธ username ni bilish')],
    [KeyboardButton(text = '๐ค ismni bilish'), KeyboardButton(text = '๐ค familiyani bilish')],
    [
      KeyboardButton(text = 'โ savolnoma yasash', request_poll=KeyboardButtonPollType(type=Poll.QUIZ)),
      KeyboardButton(text = '๐ viktorina yasash', request_poll=KeyboardButtonPollType(type=Poll.REGULAR))
    ],
    [KeyboardButton(text = "๐ orqaga")]
], resize_keyboard = True)

BUTTONS_HAVO = ReplyKeyboardMarkup([
    [KeyboardButton('๐ค Toshkent'), KeyboardButton('๐ค Namangan'), KeyboardButton('๐ค Andijon')],
    [KeyboardButton('๐ค Farg\'ona'), KeyboardButton('๐ค Sirdaryo'), KeyboardButton('๐ค Qashqadaryo')],
    [KeyboardButton('๐ค Buxoro'), KeyboardButton('๐ค Samarqand'), KeyboardButton('๐ค Jizzax')],
    [KeyboardButton('๐ค Xorazm'), KeyboardButton('๐ค Qoraqalpoq'), KeyboardButton('๐ค Navoiy')],
    [KeyboardButton(text = "๐ orqaga")]
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
    update.message.reply_text(text = "Assalomu aleykum!!! Botga xush kelibsiz! ๐", reply_markup = MENU)

def orqaga_handler(update, contaxt):
    update.message.reply_text(text = "๐ Menu", reply_markup = MENU)

def buttons_user_handler(update: Update, context: CallbackContext):
    update.message.reply_text(text="O'zingizni akkauntingiz haqida ma'lumot olish. ๐", reply_markup=BUTTONS_USER)

def buttons_havo_handler(update, context):
    update.message.reply_text(text = "Ob - havo bo'yicha ma'lumot olish. ๐", reply_markup = BUTTONS_HAVO)

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
    update.message.reply_text(text = f"<b>๐ค Namangan bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")
    
def toshkent_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/tashkent").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>๐ค Toshkent bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def andijon_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/andijan").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>๐ค Andijon bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def fergana_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/ferghana").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>๐ค Farg\'ona bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def sirdaryo_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/gulistan").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>๐ค Sirdaryo bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def qashqadaryo_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/karshi").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>๐ค Qashqadaryo bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def buxoro_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/bukhara").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>๐ค Buxoro bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def samarqand_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/samarkand").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>๐ค Samarqand bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def jizzax_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/jizzakh").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>๐ค Jizzax bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def xorazm_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/urgench").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>๐ค Xorazm bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def qoraqalpoq_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/nukus").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>๐ค Qoraqalpoq bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")

def navoiy_havo_handler(update, context):
    request = requests.get("https://obhavo.uz/navoi").text
    soup = BeautifulSoup(request, "html.parser")
    bugun = soup.find('div', class_="current-forecast")
    bugun2 = bugun.find_all('span')
    kunduzi = bugun2[1].string.strip()
    kechasi = bugun2[2].string.strip()
    update.message.reply_text(text = f"<b>๐ค Navoiy bo'yicha bugungi ob-havo ma'lumotlari\n</b><b>Kunduzi: </b>{kunduzi}\n<b>Kechasi: </b>{kechasi}", parse_mode = "HTML")


dispetcher.add_handler(CommandHandler("start", callback=start_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐จโ๐จโ๐งโ๐ฆ user haqida ma'lumot olish"), callback=buttons_user_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ค ob - havo ma'lumotlari"), callback=buttons_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ user id ni bilish"), callback=id_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("โน๏ธ username ni bilish"), callback=username_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ค ismni bilish"), callback=first_name_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ค familiyani bilish"), callback=last_name_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ orqaga"), callback=orqaga_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ต valyuta kursini bilish"), callback=valyuta_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ค Namangan"), callback=namangan_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ค Toshkent"), callback=toshkent_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ค Andijon"), callback=andijon_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ค Farg\'ona"), callback=fergana_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ค Sirdaryo"), callback=sirdaryo_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ค Qashqadaryo"), callback=qashqadaryo_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ค Buxoro"), callback=buxoro_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ค Samarqand"), callback=samarqand_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ค Jizzax"), callback=jizzax_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ค Xorazm"), callback=xorazm_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ค Qoraqalpoq"), callback=qoraqalpoq_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text("๐ค Navoiy"), callback=navoiy_havo_handler))
dispetcher.add_handler(MessageHandler(filters=Filters.text, callback=text_handler))

updater.start_polling()
updater.idle()