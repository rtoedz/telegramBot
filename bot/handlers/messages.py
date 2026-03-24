import logging
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from bot.services.openrouter import get_ai_response

LOGGER = logging.getLogger(__name__)

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    if not user_text:
        return

    # Kirim status "Typing..."
    if update.effective_chat:
        try:
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        except Exception as e:
            LOGGER.warning(f"Failed to send typing action: {e}")
    
    try:
        reply = await get_ai_response(user_text)
        await update.message.reply_text(reply)
    except Exception as e:
        LOGGER.exception("Error handling text message")
        await update.message.reply_text("Maaf, terjadi kesalahan internal saat menghubungi AI.")

def register_message_handlers(app: Application) -> None:
    # Handle semua message text yang BUKAN commands
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
