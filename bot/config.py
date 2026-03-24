import os
import re
from typing import Optional


def load_env_file(file_path: str = ".env") -> None:
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key:
                os.environ.setdefault(key, value)


def normalize_token(raw_token: str) -> Optional[str]:
    if not raw_token:
        return None

    token = raw_token.strip().strip('"').strip("'")
    return token if token else None


def get_bot_token() -> str:
    load_env_file()
    token = normalize_token(os.getenv("TELEGRAM_BOT_TOKEN", ""))
    if not token:
        raise RuntimeError(
            "Set TELEGRAM_BOT_TOKEN valid (format: angka:teks) di environment atau file .env, lalu jalankan ulang bot."
        )

    return token


def get_openrouter_key() -> str:
    load_env_file()
    key = os.getenv("OPEN_ROUTER_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "Set OPEN_ROUTER_KEY di environment atau file .env untuk menggunakan fitur AI."
        )

    return key
