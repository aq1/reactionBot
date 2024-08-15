from sqlite3 import OperationalError

from telegram import Update
from telegram.ext import CallbackContext

import db
import settings


async def sql_handler(update: Update, context: CallbackContext):
    if update.effective_chat.id != settings.ADMIN_CHAT_ID:
        return

    try:
        sql = context.match.group(1)
    except IndexError:
        return

    try:
        result = db.execute(sql)
    except OperationalError as e:
        await update.effective_message.reply_text(str(e))
        return

    if not result:
        await update.effective_message.reply_text("No result")

    text = ""
    for i, row in enumerate(result, 1):
        text += "\n" + ", ".join(map(str, row))
        if i % 10 == 0:
            await update.effective_message.reply_text(text)
            text = ""

    if not text:
        return
    await update.effective_message.reply_text(text)
