from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# Valyuta API manzili va token
EXCHANGE_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
BOT_TOKEN = "7406322804:AAGULtBXonXIQx7jaOuMXY6YnmpJx_pyUhw"

# /start komandasi
def start(update: Update, context: CallbackContext):
    button = KeyboardButton("Integratsiyaga rozilik berish.", request_contact=True)
    keyboard = [[button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        "Botdan foydalanish uchun integratsiyaga rozilik bering.",
        reply_markup=reply_markup
    )

# Telefon raqamini qayta ishlash
def contact_handler(update: Update, context: CallbackContext):
    if update.message.contact:
        button = "💵 Valyuta kursini ko‘rish"
        keyboard = [[button]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text("Ajoyib! Valyuta kurslarini endi ko‘ra olasiz.", reply_markup=reply_markup)
    else:
        update.message.reply_text("Nimadir xato! Qayta urinib ko‘ring.")

# Valyuta kurslarini ko‘rish
def show_exchange_rates(update: Update, context: CallbackContext):
    update.message.reply_text("Valyuta kurslari yuklanmoqda...")
    try:
        response = requests.get(EXCHANGE_API_URL)
        response.raise_for_status()
        data = response.json()
        rates = data["rates"]

        message = "🌍 Valyuta kurslari (USD asosida):\n\n"
        for currency, rate in rates.items():
            message += f"💵 {currency}: {rate:.2f}\n"

        update.message.reply_text(message)
    except Exception as e:
        update.message.reply_text("Valyuta kurslarini olishda xatolik yuz berdi. Kutilmagan xato.")

# Bot asosiy funksiyasi
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Handlerlar
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.contact, contact_handler))
    dp.add_handler(MessageHandler(Filters.regex("💵 Valyuta kursini ko‘rish"), show_exchange_rates))

    print("Bot ishga tushirildi...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
