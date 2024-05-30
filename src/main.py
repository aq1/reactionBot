from telegram import Update
from telegram.ext import Application, MessageReactionHandler, CommandHandler, MessageHandler, filters

import db
import settings
from handlers.log_message import log_message
from handlers.log_reaction import log_reaction
from handlers.sql_handler import sql_handler
from handlers.stats_command import stats_command


async def post_init(app: Application):
    await app.bot.send_message(
        chat_id=settings.ADMIN_CHAT_ID,
        text=f'{app.bot.username} {settings.RELEASE} started'
    )


def start_bot():
    application = Application.builder().token(
        settings.TELEGRAM_TOKEN
    ).post_init(
        post_init
    ).build()

    application.add_handler(MessageHandler(filters.ALL, log_message), group=0)

    application.add_handler(CommandHandler('stats', stats_command), group=1)
    application.add_handler(MessageReactionHandler(log_reaction), group=1)
    application.add_handler(MessageHandler(filters.Regex(r'^sql (.*)$'), sql_handler), group=1)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    db.init_db()
    start_bot()


if __name__ == '__main__':
    main()
