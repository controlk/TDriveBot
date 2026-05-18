import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ شما دسترسی ندارید")
        return
    keyboard = [[InlineKeyboardButton("📤 راهنما", callback_data='help')]]
    await update.message.reply_text("🤖 ربات TDrive آماده است\nفایل خود را فوروارد کنید", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'help':
        await query.edit_message_text("📌 راهنما:\n1. فایل خود را به ربات فوروارد کنید\n2. ربات لینک Drive را به شما می‌دهد")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("✅ فایل دریافت شد. در حال آپلود به Drive...")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.VIDEO | filters.AUDIO | filters.PHOTO | filters.Document.ALL, handle_file))
    print("✅ ربات روشن شد...")
    app.run_polling()

if __name__ == "__main__":
    main()