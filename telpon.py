import logging
import json
import uuid
import datetime
import asyncio # Kita butuh ini untuk jeda waktu
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Konfigurasi ---
TOKEN = "8065415414:AAFfy0cNR65wD_q9jfVhpxavEwGXgWgY08c" 
USER_ID = 5833267103 # Pastikan ini ID Anda
JADWAL_FILE = "jadwal.json" 

# ID Stiker Telepon Berdering (Anda bisa cari stiker lain dan dapatkan ID-nya dari bot seperti @idstickerbot)
STIKER_TELEPON = "CAACAgIAAxkBAAEGeZVmH13v_gqLgfYX73apqivJpA7nUAAC-QAD9wLID7C8A4FkP5sBHgQ"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Fungsi-fungsi utilitas (Tidak ada perubahan) ---
def simpan_jadwal(semua_jadwal):
    with open(JADWAL_FILE, 'w') as f:
        json.dump(semua_jadwal, f, indent=4)

def muat_jadwal():
    try:
        with open(JADWAL_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# --- FUNGSI PENGINGAT YANG SUDAH DIMODIFIKASI ---
async def kirim_pengingat(context: ContextTypes.DEFAULT_TYPE):
    """
    Fungsi ini sekarang melakukan simulasi panggilan yang 'berisik'.
    """
    job = context.job
    deskripsi = job.data.get("deskripsi", "Sesuatu")
    chat_id = job.chat_id
    bot = context.bot

    # 1. Pesan Awal
    pesan_awal = f"📞 **PANGGILAN MASUK!** 📞\n\nPengingat untuk: **{deskripsi}**"
    await bot.send_message(chat_id=chat_id, text=pesan_awal, parse_mode='Markdown')
    logger.info(f"Memulai simulasi panggilan untuk '{deskripsi}' ke user ID: {chat_id}")

    # 2. Kirim stiker dan pesan berulang kali
    try:
        for i in range(4): # Akan "berdering" 4 kali
            await bot.send_sticker(chat_id=chat_id, sticker=STIKER_TELEPON)
            await asyncio.sleep(2) # Jeda 2 detik
            await bot.send_message(chat_id=chat_id, text=f"_{i+1}..._ 🔊", parse_mode='Markdown')
            await asyncio.sleep(3) # Jeda 3 detik
    except Exception as e:
        logger.error(f"Gagal mengirim stiker atau pesan berulang: {e}")

    # 3. Pesan Terakhir (sebagai "panggilan tak terjawab")
    await asyncio.sleep(5) # Jeda terakhir sebelum pesan final
    pesan_akhir = f" unattended ‼️\n\nJangan lupa untuk: **{deskripsi}**"
    await bot.send_message(chat_id=chat_id, text=pesan_akhir, parse_mode='Markdown')
    logger.info(f"Simulasi panggilan untuk '{deskripsi}' selesai.")

# --- Semua Command Handler (Tidak ada perubahan) ---
async def set_jadwal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != USER_ID: return
    try:
        parts = context.args
        waktu_str = parts[0]
        deskripsi = " ".join(parts[1:])
        if not deskripsi: raise ValueError("Deskripsi kosong")
        jam, menit = map(int, waktu_str.split(':'))
        job_id = str(uuid.uuid4())
        context.job_queue.run_daily(
            callback=kirim_pengingat,
            time=datetime.time(hour=jam, minute=menit),
            chat_id=USER_ID, name=job_id, data={"deskripsi": deskripsi}
        )
        semua_jadwal = muat_jadwal()
        semua_jadwal[job_id] = {"waktu": waktu_str, "deskripsi": deskripsi, "chat_id": USER_ID}
        simpan_jadwal(semua_jadwal)
        await update.message.reply_text(f"✅ 'Panggilan' untuk '{deskripsi}' diatur setiap hari pukul {waktu_str}.")
    except (IndexError, ValueError):
        await update.message.reply_text("Format salah. Gunakan: `/set HH:MM Deskripsi`")

async def list_jadwal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != USER_ID: return
    semua_jadwal = muat_jadwal()
    if not semua_jadwal:
        await update.message.reply_text("Tidak ada jadwal yang aktif.")
        return
    pesan = "🗓️ **Jadwal 'Panggilan' Aktif:**\n\n"
    for job_id, detail in semua_jadwal.items():
        pesan += f"⏰ `{detail['waktu']}` - {detail['deskripsi']}\n   (ID: `{job_id}`)\n\n"
    await update.message.reply_text(pesan, parse_mode='Markdown')

async def delete_jadwal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != USER_ID: return
    try:
        job_id_to_delete = context.args[0]
        semua_jadwal = muat_jadwal()
        if job_id_to_delete not in semua_jadwal:
            await update.message.reply_text("ID Jadwal tidak ditemukan.")
            return
        jobs = context.job_queue.get_jobs_by_name(job_id_to_delete)
        for job in jobs: job.schedule_removal()
        deskripsi_dihapus = semua_jadwal.pop(job_id_to_delete)['deskripsi']
        simpan_jadwal(semua_jadwal)
        await update.message.reply_text(f"🗑️ Jadwal '{deskripsi_dihapus}' berhasil dihapus.")
    except IndexError:
        await update.message.reply_text("Format salah. Gunakan: `/delete ID_Jadwal`")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Halo! Aku bot pengingat pribadimu.\n\n"
        "Gunakan perintah berikut:\n"
        "`/set HH:MM Deskripsi`\n"
        "`/list`\n"
        "`/delete ID_Jadwal`", parse_mode='Markdown'
    )

def main() -> None:
    logger.info("Memulai bot...")
    # Mengatur timezone default untuk seluruh aplikasi
    application = Application.builder().token(TOKEN).build()
    job_queue = application.job_queue
    semua_jadwal = muat_jadwal()
    for job_id, detail in semua_jadwal.items():
        jam, menit = map(int, detail['waktu'].split(':'))
        job_queue.run_daily(
            callback=kirim_pengingat,
            time=datetime.time(hour=jam, minute=menit),
            chat_id=detail['chat_id'], name=job_id, data={"deskripsi": detail['deskripsi']}
        )
    logger.info(f"Berhasil memuat {len(semua_jadwal)} jadwal dari file.")
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set", set_jadwal))
    application.add_handler(CommandHandler("list", list_jadwal))
    application.add_handler(CommandHandler("delete", delete_jadwal))
    application.run_polling()
    logger.info("Bot dihentikan.")

if __name__ == "__main__":
    main()