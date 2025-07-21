import logging
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

# --- GANTI DENGAN TOKEN BARU ANDA ---
TOKEN = "8065415414:AAFfy0cNR65wD_q9jfVhpxavEwGXgWgY08c" 
USER_ID = 5833267103 

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Fungsi-fungsi Pengingat (Tidak berubah dari sebelumnya) ---
async def kirim_pesan_belajar(bot: Bot, chat_id: int):
    """Mengirim pesan pengingat belajar."""
    pesan = "🔔 **Waktunya Belajar!** 🔔\n\nAyo buka bukumu sekarang. Jangan tunda-tunda lagi, semangat!"
    await bot.send_message(chat_id=chat_id, text=pesan)
    logger.info(f"Pesan belajar terkirim ke user ID: {chat_id}")

async def simulasi_panggilan(bot: Bot, chat_id: int):
    """Mengirim pesan 'simulasi panggilan' yang lebih mencolok."""
    pesan = "☎️ **PANGGILAN PENTING** ☎️\n\nIni adalah alarm belajarmu! Anggap saja ini panggilan dari masa depanmu yang sukses. Ayo, segera belajar!"
    await bot.send_message(chat_id=chat_id, text=pesan)
    logger.info(f"Simulasi panggilan terkirim ke user ID: {chat_id}")

# --- Fungsi Command Handler (Tidak berubah) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mengirim pesan sapaan ketika command /start dijalankan."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Halo {user.mention_html()}! 👋 Aku adalah Asisten Belajar Pribadimu."
    )
    logger.info(f"Bot di-start oleh user: {user.first_name} (ID: {user.id})")

# --- PERBAIKAN UTAMA: FUNGSI UNTUK SCHEDULER ---
async def post_init(application: Application):
    """Fungsi yang dijalankan setelah bot siap untuk memulai scheduler."""
    scheduler = AsyncIOScheduler(timezone=timezone("Asia/Jakarta"))
    scheduler.add_job(
        kirim_pesan_belajar, 
        'cron', 
        hour=19, 
        minute=0, 
        kwargs={"bot": application.bot, "chat_id": USER_ID}
    )
    scheduler.add_job(
        simulasi_panggilan, 
        'cron', 
        hour=20, 
        minute=0, 
        kwargs={"bot": application.bot, "chat_id": USER_ID}
    )
    scheduler.start()
    logger.info("Scheduler berhasil dimulai. Jadwal aktif:")
    scheduler.print_jobs()

def main() -> None:
    """Fungsi utama untuk menjalankan bot."""
    logger.info("Memulai bot...")
    
    # Beritahu builder untuk menjalankan post_init setelah siap
    application = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init) # <-- Kunci perbaikannya di sini
        .build()
    )

    # Tambahkan handler seperti biasa
    application.add_handler(CommandHandler("start", start))

    # Jalankan bot.
    application.run_polling()
    
    logger.info("Bot dihentikan.")

if __name__ == "__main__":
    main()