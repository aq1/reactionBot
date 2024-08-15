from sqlite3 import OperationalError

from telegram import Update
from telegram.ext import CallbackContext

from prettytable import from_db_cursor

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
        cursor = db.get_cursor()
        cursor.execute(sql)
    except OperationalError as e:
        await update.effective_message.reply_text(str(e))
        return

    table = from_db_cursor(cursor)
    if not table:
        return

    i = 0
    while i < len(table.rows):
        await update.effective_message.reply_text(
            text=f"<code>{table.get_string(start=i, end=i + 10)}</code>",
        )
        i += 10
