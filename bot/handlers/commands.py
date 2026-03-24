from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"Halo {user_name}! Bot kamu sudah aktif di Mac.")


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Made by Edz")


async def task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("sekarang kamu mempunyai Task :\n1. blablalba")


def register_command_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("task", task))
