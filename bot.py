import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ===============================
# KEYBOARD
# ===============================
def get_keyboard():
    keyboard = [
        [InlineKeyboardButton("OKE", callback_data="oke")],
        [InlineKeyboardButton("🔄 Refresh", callback_data="retry")]
    ]
    return InlineKeyboardMarkup(keyboard)


# ===============================
# START
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name

    await update.message.reply_text(
        f"<b>Halo {name}</b> 👋\n\n"
        "Selamat datang di <b>Pemersatu Bangsa</b>\n\n"
        "Untuk mendapatkan <b>500 file</b> yang akan saya bagikan,\n"
        "wajib mengikuti misi dibawah ya.\n\n"
        "Silakan tekan OKE 👇",
        reply_markup=get_keyboard(),
        parse_mode="HTML"
    )


# ===============================
# BUTTON HANDLER
# ===============================
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "oke":
        text = (
            "📌 <b>MISI WAJIB DISELESAIKAN</b>\n\n"
            "🔗 Link pendaftaran:\n"
            "https://puzzlefarm.shareearn1.com/?code=11350521\n\n"
            "✅ Login lewat FB biar dapat coin lebih\n"
            "✅ Kerjain misinya\n"
            "✅ Rajin login biar dapat reward banyak\n\n"
            "🚀 WAJIB MASUKIN ID REFFERAL = <b>11350521</b>"
        )

        await query.edit_message_text(
            text,
            reply_markup=get_keyboard(),
            parse_mode="HTML"
        )

    elif query.data == "retry":
        # Kirim pesan BARU (bukan edit)
        await query.message.reply_text(
            "❌ Kamu belum menyelesaikan misinya!\n\n"
            "🚀 WAJIB MASUKIN ID REFFERAL = 11350521\n\n"
            "Selesaikan dulu misinya biar 500 file bisa kebuka!",
            reply_markup=get_keyboard()
        )


# ===============================
# MAIN
# ===============================
def main():
    if not BOT_TOKEN:
        print("TOKEN belum diisi!")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))

    print("Bot aktif bro 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()
