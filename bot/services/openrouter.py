from openai import AsyncOpenAI
from bot.config import get_openrouter_key

async def get_ai_response(prompt: str) -> str:
    key = get_openrouter_key()
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=key,
    )
    
    try:
        response = await client.chat.completions.create(
            model="stepfun/step-3.5-flash:free",
            messages=[
                {
                    "role": "system",
                    "content": "Kamu adalah asisten AI yang ramah dan membantu untuk pengguna Telegram."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )
        return response.choices[0].message.content or "Maaf, saya tidak bisa memberikan jawaban saat ini."
    except Exception as e:
        return f"Terjadi kesalahan saat menghubungi layanan AI: {str(e)}"
