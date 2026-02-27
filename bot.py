import os
import logging
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
    user = update.effective_user
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
            "✅ Wajib login menggunakan <b>Facebook</b>\n"
            "🔒 Tenang, tidak ada input ID atau password di dalam game,\n"
            "cukup konek akun FB dengan game tersebut.\n\n"
            "✅ Wajib capai <b>90.000 coin</b>\n"
            "📸 Setelah mencapai 90.000 coin wajib kirim screenshot bukti\n\n"
            "🚀 WAJIB MASUKIN ID REFFERAL = <b>11350521</b>\n\n"
            "🎁 Semua ini GRATIS untuk akses 1000 file."
        )

        await query.edit_message_caption(
            caption=text,
            reply_markup=get_keyboard(),
            parse_mode="HTML"
        )

    elif query.data == "retry":
        await query.message.reply_text(
            "❌ Kamu belum menyelesaikan misinya!\n\n"
            "📌 Cara masukkan ID Referral:\n"
            "1️⃣ Buka game dari link tadi\n"
            "2️⃣ Masuk ke bagian <b>Invite</b>\n"
            "3️⃣ Di bagian 'Yang Mengundang Saya' isi dengan:\n"
            "👉 <b>11350521</b>\n\n"
            "🎯 Wajib login pakai Facebook\n"
            "🎯 Wajib capai 90.000 coin\n"
            "📸 Setelah itu kirim screenshot bukti ke bot ini!",
            reply_markup=get_keyboard(),
            parse_mode="HTML"
        )


# ===============================
# HANDLE FOTO (AUTO BALAS JIKA KIRIM SCREENSHOT)
# ===============================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Kamu belum menyelesaikan misinya!\n\n"
        "📌 Pastikan sudah:\n"
        "✅ Login pakai Facebook\n"
        "✅ Masukkan ID Referral 11350521 di menu Invite\n"
        "✅ Capai 90.000 coin\n\n"
        "Jika sudah memenuhi semua syarat, tunggu verifikasi admin.",
        reply_markup=get_keyboard(),
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
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot aktif bro 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()
