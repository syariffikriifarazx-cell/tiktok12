import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
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
# CHANNEL PRIVATE KAMU
# ===============================
CHANNEL_ID = -1003892236146

# ===============================
# KEYBOARD 1 TOMBOL
# ===============================
def get_start_keyboard():
    keyboard = [
        [InlineKeyboardButton("OKE", callback_data="show_videos")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ===============================
# START COMMAND
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name  # hanya pakai nama tampilan

    await update.message.reply_text(
        f"<b>Halo {name}</b> 👋\n\n"
        "Selamat datang di Bot Asupan Lokal.\n\n"
        "Cara untuk mengakses semua file,\n"
        "Ada di bawah ya 👇",
        reply_markup=get_start_keyboard(),
        parse_mode="HTML"
    )

# ===============================
# HANDLE BUTTON
# ===============================
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "show_videos":

        await query.edit_message_text("📦 Mengirim 100 file... sabar ya bro 🔥")

        message_ids = list(range(2, 34))

        for msg_id in message_ids:
            await context.bot.copy_message(
                chat_id=query.message.chat_id,
                from_chat_id=CHANNEL_ID,
                message_id=msg_id
            )
            await asyncio.sleep(0.7)

# ===============================
# MAIN
# ===============================
def main():
    if not BOT_TOKEN:
        print("TOKEN belum diisi di file .env!")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))

    print("Bot aktif bro 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()