import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ===============================
# ADMIN & FILE STORAGE
# ===============================
ADMIN_ID = 7640270845
USER_FILE = "users.txt"


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
# SAVE USER (PERMANENT)
# ===============================
def save_user(user_id):
    today = datetime.now().strftime("%Y-%m-%d")

    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            for line in f:
                uid, date = line.strip().split("|")
                users[int(uid)] = date

    if user_id not in users:
        with open(USER_FILE, "a") as f:
            f.write(f"{user_id}|{today}\n")


# ===============================
# START
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)

    name = user.last_name if user.last_name else user.first_name

    caption_text = (
        f"<b>Halo {name}</b> 👋\n\n"
        "Selamat datang di <b>Pemersatu Bangsa</b>\n\n"
        "Untuk mendapatkan <b>1000 file</b> yang akan saya bagikan,\n"
        "wajib mengikuti misi dibawah ya.\n\n"
        "Silakan tekan OKE 👇"
    )

    sent_msg = await context.bot.copy_message(
        chat_id=update.effective_chat.id,
        from_chat_id=-1003834385991,
        message_id=2
    )

    await context.bot.edit_message_caption(
        chat_id=update.effective_chat.id,
        message_id=sent_msg.message_id,
        caption=caption_text,
        reply_markup=get_keyboard(),
        parse_mode="HTML"
    )


# ===============================
# STATISTIK BOT (ADMIN ONLY)
# ===============================
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Kamu bukan admin.")
        return

    if not os.path.exists(USER_FILE):
        await update.message.reply_text("Belum ada user.")
        return

    total = 0
    today_count = 0
    yesterday_count = 0

    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    with open(USER_FILE, "r") as f:
        for line in f:
            uid, date = line.strip().split("|")
            total += 1
            if date == today:
                today_count += 1
            if date == yesterday:
                yesterday_count += 1

    text = (
        "📊 <b>Statistik Bot</b>\n\n"
        f"Total User: {total}\n"
        f"User Hari Ini: {today_count}\n"
        f"User Kemarin: {yesterday_count}"
    )

    await update.message.reply_text(text, parse_mode="HTML")


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
            "1️⃣ Wajib login menggunakan <b>Facebook</b>\n"
            "2️⃣ Wajib mencapai <b>229.000 coin</b>\n"
            "3️⃣ Kirim bukti screenshot di bot ini\n"
            "4️⃣ File akan dikirim setelah verifikasi\n\n"
            "🎁 Semua ini GRATIS untuk akses 1000 file."
        )

        await query.message.reply_text(
            text,
            reply_markup=get_keyboard(),
            parse_mode="HTML"
        )

    elif query.data == "retry":
        await query.message.reply_text(
            "❌ <b>Misi Belum Selesai</b>\n\n"
            "Silakan selesaikan misinya dulu ya.",
            reply_markup=get_keyboard(),
            parse_mode="HTML"
        )


# ===============================
# HANDLE FOTO
# ===============================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.copy_message(
        chat_id=update.effective_chat.id,
        from_chat_id=-1003834385991,
        message_id=3,
        caption=(
            "❌ <b>COIN belum memenuhi syarat.</b>\n\n"
            "Naikin coin sampai 229.000 lalu kirim ulang screenshot."
        ),
        parse_mode="HTML"
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
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot aktif bro 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()
