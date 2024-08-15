from telegram import Update, User

import db


def update_or_create_user(user: User):
    user_exists = len(
        db.execute("select id from telegram_user where id = ?", arguments=(user.id,))
    )

    if not user_exists:
        db.execute(
            "insert into telegram_user(id, username, fullname) values (?, ?, ?)",
            (user.id, user.username, user.full_name),
        )
    else:
        db.execute(
            "update telegram_user set username=?, fullname=? where id=?",
            (user.username, user.full_name, user.id),
        )


async def log_message(update: Update, _):
    update_or_create_user(update.effective_user)

    if update.effective_chat.id > 0:
        return

    db.execute(
        "insert into message(chat_id, message_id, user_id) values(?, ?, ?)",
        (
            update.effective_chat.id,
            update.effective_message.id,
            update.effective_user.id,
        ),
    )
