import logging
import time
import re
import phonenumbers
from phonenumbers import geocoder
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests

# --- KONFIGURASI (GANTI DENGAN DATA BARU) ---
TOKEN = "8906788061:AAGEaBf-iweuMEuE-rzH833MqsNWQOwQngQ"
GROUP_ID = "-1003977204948"
OWNER_ID = 8764955504
API_URL = "https://wilz-api.vercel.app/api/banding"
API_KEY = "wilzfree"
EMAIL = "wilzfixmerah1@gmail.com"
APP_PW = "ipktzcggjemrbvfc"

# --- STATUS GLOBAL ---
user_languages = {} 
SEND_NOTIF_TO_GROUP = True
last_command_time = 0
COOLDOWN_TIME = 60

# --- TEKS MULTI-BAHASA ---
TEXTS = {
    "id": {
        "start": "Halo! Bot siap. Gunakan /f <nomor> untuk mulai.",
        "lang_changed": "Bahasa diubah ke Bahasa Indonesia.",
        "cooldown": "⏳ Harap tunggu {time} detik lagi.",
        "usage": "⚠️ Format salah!\n\nCara pakai:\nKetik: `/f <nomor_telepon>`\nContoh: `/f +628123456789`",
        "processing": "⏳ Memproses: {nomor}...",
        "success": "✅ Berhasil",
        "failed": "❌ Gagal"
    },
    "en": {
        "start": "Hello! Bot is ready. Use /f <number> to start.",
        "lang_changed": "Language changed to English.",
        "cooldown": "⏳ Please wait {time} seconds.",
        "usage": "⚠️ Wrong format!\n\nUsage:\nType: `/f <phone_number>`\nExample: `/f +628123456789`",
        "processing": "⏳ Processing: {nomor}...",
        "success": "✅ Success",
        "failed": "❌ Failed"
    }
}

def get_text(user_id, key):
    lang = user_languages.get(user_id, "id")
    return TEXTS[lang][key]

# --- FUNGSI PEMBANTU ---
def clean_phone_number(input_str):
    return '+' + re.sub(r'\D', '', input_str)

def get_country(phone_str):
    try:
        parsed = phonenumbers.parse(phone_str if phone_str.startswith('+') else '+' + phone_str, None)
        return geocoder.country_name_for_number(parsed, "id") or "Tidak Diketahui"
    except: return "Tidak Diketahui"

def sensor_nomor(nomor):
    return nomor[:5] + "******" + nomor[-3:] if len(nomor) > 8 else "******"

# --- HANDLER ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇮🇩 Indonesia", callback_data="id"),
         InlineKeyboardButton("🇬🇧 English", callback_data="en")]
    ]
    await update.message.reply_text(
        get_text(update.effective_user.id, "start"),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_languages[query.from_user.id] = query.data
    await query.answer()
    await query.edit_message_text(get_text(query.from_user.id, "lang_changed"))

async def toggle_notif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global SEND_NOTIF_TO_GROUP
    if update.effective_user.id != OWNER_ID: return
    SEND_NOTIF_TO_GROUP = not SEND_NOTIF_TO_GROUP
    await update.message.reply_text(f"Notif Grup: {'ON' if SEND_NOTIF_TO_GROUP else 'OFF'}")

async def f_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_command_time
    uid = update.effective_user.id
    if uid != OWNER_ID: return

    if not context.args:
        await update.message.reply_text(get_text(uid, "usage"), parse_mode='Markdown')
        return

    current_time = time.time()
    if current_time - last_command_time < COOLDOWN_TIME:
        rem = int(COOLDOWN_TIME - (current_time - last_command_time))
        await update.message.reply_text(get_text(uid, "cooldown").format(time=rem))
        return

    nomor_final = clean_phone_number(" ".join(context.args))
    negara = get_country(nomor_final)
    last_command_time = current_time

    msg = await update.message.reply_text(get_text(uid, "processing").format(nomor=sensor_nomor(nomor_final)))

    try:
        resp = requests.get(API_URL, params={"apikey": API_KEY, "email": EMAIL, "app_pw": APP_PW, "pesan": nomor_final}).json()
        is_success = resp.get("status")
        status_txt = resp.get('message', 'No response')
        
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id, message_id=msg.message_id,
            text=f"{get_text(uid, 'success' if is_success else 'failed')}: {status_txt}"
        )

        # Bagian job_queue telah dihapus agar tidak error
        if SEND_NOTIF_TO_GROUP:
            await context.bot.send_message(chat_id=GROUP_ID, text=f"🔔 Status: {'Berhasil' if is_success else 'Gagal'}\nNomor: `{sensor_nomor(nomor_final)}`\nNegara: {negara}\nRespon: {status_txt}", parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("f", f_handler))
    app.add_handler(CommandHandler("toggle_notif", toggle_notif))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("BOT FIX MERAH FREE BY @Teamwilz Online...")
    app.run_polling()