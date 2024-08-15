from sqlite3 import OperationalError

from telegram import Update
from telegram.ext import CallbackContext

from prettytable import PrettyTable

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
        result, cursor = db.execute(sql)
    except OperationalError as e:
        await update.effective_message.reply_text(str(e))
        return

    if not result:
        await update.effective_message.reply_text("No result")

    table = PrettyTable(
        field_names=[desc[0] for desc in cursor.description],
    )
    for i, row in enumerate(result, 1):
        table.add_row(row)
        if i % 10 == 0:
            await update.effective_message.reply_text(f"<code>{table}</code>")
            table = PrettyTable(
                field_names=[desc[0] for desc in cursor.description],
            )

    if not table.rows:
        return
    await update.effective_message.reply_text(f"<code>{table}</code>")
