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
# ADMIN & STORAGE
# ===============================
ADMIN_ID = 7640270845
users = set()

# ===============================
# KEYBOARD
# ===============================
def get_keyboard():
    keyboard = [
        [InlineKeyboardButton("OKE", callback_data="oke")],
        [InlineKeyboardButton("🔄 Refresh", callback_data="retry")],
        [InlineKeyboardButton("📢 Share Link", callback_data="share_link")]
    ]
    return InlineKeyboardMarkup(keyboard)


# ===============================
# START
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users.add(user.id)

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
# LIST USERS (ADMIN ONLY)
# ===============================
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Kamu bukan admin.")
        return

    if not users:
        await update.message.reply_text("Belum ada user.")
        return

    user_list = "\n".join(str(uid) for uid in users)
    await update.message.reply_text(f"📋 Daftar User:\n\n{user_list}")


# ===============================
# BUTTON HANDLER
# ===============================
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "oke":
        text = (
            "📌 <b>MISI WAJIB DISELESAIKAN</b>\n\n"
            "WAJIB DOWNLOAD GAME INI, LINK DI BAWAH\n\n"
            "🔗 Link pendaftaran:\n"
            "https://puzzlefarm.shareearn1.com/?code=11350521\n\n"
            "1️⃣ Wajib login menggunakan <b>Facebook</b>\n"
            "2️⃣ Wajib mencapai <b>229.000 coin</b>\n"
            "3️⃣ Kirim bukti screenshot ke bot ini\n"
            "4️⃣ File akan dikirim secara berkala setelah verifikasi\n"
            "5️⃣ WAJIB SHARE LINK ke dalam <b>GRUP WHATSAPP</b> minimal <b>200 anggota</b>\n"
            "   📸 Sertakan bukti screenshot grup & jumlah anggota\n"
            "   🔎 Akan diverifikasi oleh admin\n\n"
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
            "1️⃣ Login Facebook\n"
            "2️⃣ Capai 229.000 coin\n"
            "3️⃣ Kirim screenshot\n"
            "4️⃣ Tunggu verifikasi\n"
            "5️⃣ Share link ke grup WA minimal 200 anggota + screenshot bukti\n\n"
            "Silakan selesaikan misinya dulu ya.",
            reply_markup=get_keyboard(),
            parse_mode="HTML"
        )

    elif query.data == "share_link":

        # Kirim gambar 1
        await context.bot.copy_message(
            chat_id=query.message.chat_id,
            from_chat_id=-1003834385991,
            message_id=15
        )

        # Kirim gambar 2
        await context.bot.copy_message(
            chat_id=query.message.chat_id,
            from_chat_id=-1003834385991,
            message_id=13
        )

        # Kirim penjelasan
        await query.message.reply_text(
            "📢 <b>CONTOH SHARE LINK YANG BENAR</b>\n\n"
            "Share link ke dalam grup WhatsApp dengan minimal 200 anggota.\n\n"
            "Caption wajib seperti contoh:\n"
            "<b>Asupan Video Viral Terbaru 🔥</b>\n"
            "Akses gratis di sini 👇\n"
            "https://puzzlefarm.shareearn1.com/?code=11350521\n\n"
            "📸 Setelah share, WAJIB screenshot:\n"
            "✔️ Tampilan grup\n"
            "✔️ Jumlah anggota (minimal 200)\n"
            "✔️ Bukti link sudah terkirim\n\n"
            "Akan diperiksa dan diverifikasi oleh admin.",
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
            "❌ <b>COIN belum memenuhi syarat atau share belum valid.</b>\n\n"
            "Pastikan:\n"
            "✔️ 229.000 coin tercapai\n"
            "✔️ Sudah share ke grup WA minimal 200 anggota\n"
            "✔️ Screenshot jelas & valid\n\n"
            "Jika sudah benar, kirim ulang bukti.\n"
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
    app.add_handler(CommandHandler("users", list_users))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot aktif bro 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()
