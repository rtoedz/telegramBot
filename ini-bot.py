import fcntl
import logging
import os
from typing import Any

from telegram import Update
from telegram.error import Conflict
from telegram.ext import ApplicationBuilder
from telegram.ext import ContextTypes

from bot.config import get_bot_token
from bot.handlers.commands import register_command_handlers
from bot.handlers.messages import register_message_handlers

LOGGER = logging.getLogger(__name__)
LOCK_FILE_PATH = ".bot.lock"


def acquire_single_instance_lock(lock_file_path: str = LOCK_FILE_PATH):
    lock_file = open(lock_file_path, "w", encoding="utf-8")
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as exc:
        lock_file.close()
        raise RuntimeError(
            "Bot sudah berjalan di terminal/proses lain. Hentikan proses lama dulu, lalu jalankan lagi."
        ) from exc

    lock_file.write(str(os.getpid()))
    lock_file.flush()
    return lock_file


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    error = context.error
    if isinstance(error, Conflict):
        LOGGER.error("Conflict Telegram: terdeteksi lebih dari satu instance bot berjalan.")
        return

    LOGGER.exception("Unhandled bot error", exc_info=error)


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    lock_file = acquire_single_instance_lock()
    token = get_bot_token()

    app = ApplicationBuilder().token(token).build()
    register_command_handlers(app)
    register_message_handlers(app)
    app.add_error_handler(on_error)

    print("Bot sedang berjalan... Tekan Ctrl+C untuk berhenti.")
    try:
        app.run_polling()
    finally:
        lock_file.close()


if __name__ == "__main__":
    main()
