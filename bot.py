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
            "1️⃣ Wajib login menggunakan <b>Facebook</b>\n"
            "🔒 Tenang, tidak ada input ID atau password di dalam game, hanya konek lewat game.\n"
            "2️⃣ Wajib mencapai <b>229.000 coin</b> (Akan diverifikasi oleh admin, tidak bisa curang)\n"
            "3️⃣ Setelah itu kirim bukti screenshot di bot ini (Akan segera diverifikasi admin)\n"
            "4️⃣ Setelah semuanya beres file akan dikirim secara berkala\n\n"
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
            "1️⃣ Wajib login menggunakan Facebook\n"
            "2️⃣ Wajib mencapai <b>229.000 coin</b> (Diverifikasi admin)\n"
            "3️⃣ Kirim bukti screenshot di bot ini\n"
            "4️⃣ File akan dikirim secara berkala setelah verifikasi\n\n"
            "Silakan selesaikan misinya dulu ya.",
            reply_markup=get_keyboard(),
            parse_mode="HTML"
        )


# ===============================
# HANDLE FOTO (KIRIM GAMBAR + CAPTION)
# ===============================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.copy_message(
        chat_id=update.effective_chat.id,
        from_chat_id=-1003834385991,  # GANTI jika beda channel
        message_id=3,  # ID dari link https://t.me/c/3834385991/3
        caption=(
            "❌ <b>COIN yang kamu peroleh belum memenuhi syarat.</b>\n\n"
            "Harap naikin coin di dalam game tadi sebanyak <b>229.000 coin</b>.\n\n"
            "Jika sudah memenuhi syarat, kirim bukti screenshot kembali.\n"
            "Akan segera diverifikasi admin.\n\n"
            "Terimakasih."
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
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot aktif bro 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()
