import asyncio

import telegram

import settings


def send_message(text):
    asyncio.run(
        telegram.Bot(
            token=settings.TELEGRAM_TOKEN,
        ).send_message(
            chat_id=settings.TELEGRAM_CHAT_ID,
            text=text,
        )
    )
