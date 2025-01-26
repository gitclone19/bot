from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
import requests

# Valyuta API manzili va token
EXCHANGE_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"  # Valyuta API manzili
BOT_TOKEN = "7406322804:AAGULtBXonXIQx7jaOuMXY6YnmpJx_pyUhw"  # Bot tokeningizni kiriting

# /start komandasi
async def start(update: Update, context: CallbackContext) -> None:                                                                                            button = KeyboardButton("Integratsiyaga rozilik berish.", request_contact=True)
    keyboard = [[button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Botdan foydalanish uchun integratsiyaga rozilik bering.",
        reply_markup=reply_markup
    )

# Telefon raqamini qayta ishlash                                                                                                                          async def contact_handler(update: Update, context: CallbackContext) -> None:
    if update.message.contact:
        button = "💵 Valyuta kursini ko‘rish"
        keyboard = [[button]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Ajoyib! Valyuta kurslarini endi ko‘ra olasiz.", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Nimadir xato! Qayta urinib ko‘ring.")

# Valyuta kurslarini ko‘rish
async def show_exchange_rates(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Valyuta kurslari yuklanmoqda...")
    try:
        # Valyuta API'ga so‘rov yuborish
        response = requests.get(EXCHANGE_API_URL)
        response.raise_for_status()  # Xatolik bo'lsa, exception tashlaydi
        data = response.json()
        rates = data["rates"]

        # Kurslarni chiqarish
        message = "🌍 Valyuta kurslari (USD asosida):\n\n"
        for currency, rate in rates.items():
            message += f"💵 {currency}: {rate:.2f}\n"

        await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text("Valyuta kurslarini olishda xatolik yuz berdi. Kutilmagan xato.")

# Bot asosiy funksiyasi
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlerlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(MessageHandler(filters.Regex("💵 Valyuta kursini ko‘rish"), show_exchange_rates))

    print("Bot ishga tushirildi...")
    app.run_polling()

if name == "main":
    main()
