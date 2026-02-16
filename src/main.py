import re

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    Defaults,
    MessageHandler,
    MessageReactionHandler,
    filters,
)

import db
import settings
from handlers.log_message import log_message
from handlers.log_reaction import log_reaction
from handlers.social_link_handler import social_link_handler
from handlers.sql_handler import sql_handler
from handlers.stats_command import stats_command


async def post_init(app: Application):
    await app.bot.send_message(
        chat_id=settings.ADMIN_CHAT_ID,
        text=f"{app.bot.username} {settings.RELEASE} started",
    )


def start_bot():
    application = (
        Application.builder()
        .token(settings.TELEGRAM_TOKEN)
        .post_init(post_init)
        .defaults(Defaults(parse_mode=ParseMode.HTML))
        .build()
    )

    application.add_handler(MessageHandler(filters.ALL, log_message), group=0)

    application.add_handler(
        MessageHandler(
            filters.Regex(re.compile(r"^sql ([\s\S]+)$", re.MULTILINE)), sql_handler
        ),
        group=1,
    )
    application.add_handler(CommandHandler("stats", stats_command), group=1)
    application.add_handler(
        MessageHandler(filters.Entity("url"), social_link_handler), group=1
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    db.init_db()
    start_bot()


if __name__ == "__main__":
    main()
