from telegram import Update


async def stats_command(update: Update, _):
    await update.effective_chat.send_message("WIP")
