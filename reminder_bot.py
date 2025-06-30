import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

# --- Konfigurasi Penting ---
# Ambil data dari Environment Variables. Kode ini akan error jika dijalankan 
# di komputer lokal tanpa setting env vars, tapi akan bekerja di server.
try:
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    USER_ID = int(os.environ.get("TELEGRAM_USER_ID"))
    if not TOKEN or not USER_ID:
        raise ValueError("TELEGRAM_TOKEN atau TELEGRAM_USER_ID tidak ditemukan di environment variables.")
except (TypeError, ValueError) as e:
    print(f"Error: {e}")
    print("Pastikan Anda sudah mengatur TELEGRAM_TOKEN dan TELEGRAM_USER_ID sebagai environment variable.")
    exit() # Keluar dari program jika variabel tidak diset

# Mengaktifkan logging untuk melihat aktivitas bot dan error
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Fungsi-fungsi Pengingat ---

async def kirim_pesan_belajar(context: ContextTypes.DEFAULT_TYPE):
    """Mengirim pesan pengingat belajar."""
    job = context.job
    pesan = "🔔 **Waktunya Belajar!** 🔔\n\nAyo buka bukumu sekarang. Jangan tunda-tunda lagi, semangat!"
    await context.bot.send_message(job.chat_id, text=pesan, parse_mode='MarkdownV2')
    logger.info(f"Pesan belajar terkirim ke user ID: {job.chat_id}")

async def simulasi_panggilan(context: ContextTypes.DEFAULT_TYPE):
    """Mengirim pesan 'simulasi panggilan' yang lebih mencolok."""
    job = context.job
    pesan = "☎️ **PANGGILAN PENTING** ☎️\n\nIni adalah alarm belajarmu\! Anggap saja ini panggilan dari masa depanmu yang sukses\. Ayo, segera belajar\!"
    # Catatan: Karakter seperti '!' atau '.' perlu di-escape dengan '\' dalam mode MarkdownV2
    await context.bot.send_message(job.chat_id, text=pesan, parse_mode='MarkdownV2')
    logger.info(f"Simulasi panggilan terkirim ke user ID: {job.chat_id}")


# --- Fungsi Command Handler ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mengirim pesan sapaan ketika command /start dijalankan."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Halo {user.mention_html()}! 👋 Aku adalah Asisten Belajar Pribadimu. "
        "Aku sudah aktif dan akan mengingatkanmu sesuai jadwal yang telah ditentukan."
    )
    logger.info(f"Bot di-start oleh user: {user.first_name} (ID: {user.id})")

def main() -> None:
    """Fungsi utama untuk menjalankan bot dan scheduler."""
    logger.info("Memulai bot...")

    # Buat aplikasi bot
    application = Application.builder().token(TOKEN).build()

    # Tambahkan handler untuk command /start
    application.add_handler(CommandHandler("start", start))

    # Buat scheduler dengan zona waktu yang benar
    # Menggunakan pytz untuk zona waktu yang lebih stabil
    scheduler = AsyncIOScheduler(timezone=timezone("Asia/Jakarta"))
    
    # --- Atur Jadwal Pengingat di Sini ---
    
    # Jadwal 1: Kirim pesan biasa jam 19:00 WIB setiap hari
    scheduler.add_job(
        kirim_pesan_belajar, 
        'cron', 
        hour=19, 
        minute=0, 
        kwargs={"chat_id": USER_ID}
    )
    
    # Jadwal 2: Kirim "simulasi panggilan" jam 20:00 WIB setiap hari
    scheduler.add_job(
        simulasi_panggilan, 
        'cron', 
        hour=20, 
        minute=0, 
        kwargs={"chat_id": USER_ID}
    )

    # Mulai scheduler
    scheduler.start()
    logger.info("Scheduler berhasil dimulai. Jadwal aktif:")
    scheduler.print_jobs()

    # Jalankan bot
    application.run_polling()
    
    logger.info("Bot dihentikan.")

if __name__ == "__main__":
    main()