from telegram import Update


async def stats_command(update: Update, _):
    await update.effective_message.reply_text('Coming soon')
