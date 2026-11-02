import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

files = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Welcome to All In One Bot!\n\n"
        "📥 Send files to share them.\n"
        "🎬 Send videos.\n"
        "🎵 Send audio.\n\n"
        "Commands:\n"
        "/start - Start Bot\n"
        "/help - Help\n"
        "/files - Your uploaded files\n"
        "/id - Your Telegram ID\n"
        "/announce - Admin announcement"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 All In One Bot Help\n\n"
        "📂 Send documents to the bot.\n"
        "🎬 Send videos to the bot.\n"
        "🎵 Send audio to the bot.\n"
        "📁 Use /files to see uploaded files."
    )

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Your Telegram ID: {update.effective_user.id}"
    )

async def receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if msg.document:
        files.append(("document", msg.document.file_id))
        name = msg.document.file_name

    elif msg.video:
        files.append(("video", msg.video.file_id))
        name = "Video"

    elif msg.audio:
        files.append(("audio", msg.audio.file_id))
        name = "Audio"

    elif msg.photo:
        files.append(("photo", msg.photo[-1].file_id))
        name = "Photo"

    else:
        return

    await msg.reply_text(
        f"✅ File received!\n📁 {name}\n"
        "Use /files to see your uploaded files."
    )

async def show_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not files:
        await update.message.reply_text("No files uploaded yet.")
        return

    for file_type, file_id in files[-10:]:
        if file_type == "document":
            await context.bot.send_document(
                update.effective_chat.id, file_id
            )
        elif file_type == "video":
            await context.bot.send_video(
                update.effective_chat.id, file_id
            )
        elif file_type == "audio":
            await context.bot.send_audio(
                update.effective_chat.id, file_id
            )
        elif file_type == "photo":
            await context.bot.send_photo(
                update.effective_chat.id, file_id
            )

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Thanks for messaging!\n"
        "🤖 I am All In One Bot.\n"
        "Type /help to see my features."
    )

async def announce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Admin only!")
        return

    message = " ".join(context.args)

    if not message:
        await update.message.reply_text(
            "Usage: /announce Your message"
        )
        return

    await update.message.reply_text(
        "📢 Announcement feature is ready. "
        "Configure your channel ID to publish announcements."
    )

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is missing!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("files", show_files))
    app.add_handler(CommandHandler("announce", announce))

    app.add_handler(
        MessageHandler(
            filters.Document.ALL | filters.VIDEO |
            filters.AUDIO | filters.PHOTO,
            receive_file
        )
    )

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply)
    )

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
