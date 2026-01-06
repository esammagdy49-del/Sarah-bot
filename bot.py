import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters
)

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

users_waiting = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💬 ابعت صراحة", callback_data="send")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 أهلاً بيك في بوت الصراحة\n"
        "اضغط على الزر وبعت اللي في بالك براحتك 🤍",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "send":
        users_waiting.add(query.from_user.id)
        await query.message.reply_text("✍️ اكتب رسالتك دلوقتي:")

async def receive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id in users_waiting:
        users_waiting.remove(user_id)
        msg = update.message.text

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 صراحة جديدة:\n\n{msg}"
        )

        await update.message.reply_text("✅ تم إرسال الصراحة بنجاح 🤍")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive))

app.run_polling()
