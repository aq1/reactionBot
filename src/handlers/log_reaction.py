from typing import Sequence

from telegram import Update, ReactionType

from src import (
    db,
)


def add_reaction(chat_id: int, user_id: int, emoji_id: str, count: int):
    emoji = db.execute(
        'select id from stat where user_id=? and chat_id=? and emoji_id=?',
        (user_id, chat_id, emoji_id),
    )

    if len(emoji) == 0:
        db.execute(
            'insert into stat(user_id, chat_id, emoji_id, count) values(?, ?, ?, ?)',
            (user_id, chat_id, emoji_id, max(0, count)),
        )
    else:
        db.execute(
            'update stat set count=count + ? where user_id=? and chat_id=? and emoji_id=?',
            (count, user_id, chat_id, emoji_id),
        )


async def log_reaction(update: Update, _):
    old: Sequence[ReactionType] = []
    new: Sequence[ReactionType] = []

    if hasattr(update.message_reaction, 'old_reaction'):
        old = update.message_reaction.old_reaction

    if hasattr(update.message_reaction, 'new_reaction'):
        new = update.message_reaction.new_reaction

    for count, reactions in zip((-1, 1), (old, new)):
        for reaction in reactions:
            if reaction.type == ReactionType.CUSTOM_EMOJI:
                emoji_id = reaction.custom_emoji_id
            else:
                emoji_id = reaction.emoji

            message = db.execute(
                'select user_id from message where chat_id=? and message_id=?',
                (update.message_reaction.chat.id, update.message_reaction.message_id)
            )
            if not message:
                continue

            user_id = message[0][0]

            if user_id == update.effective_user.id:
                continue

            add_reaction(
                chat_id=update.effective_chat.id,
                user_id=user_id,
                emoji_id=emoji_id,
                count=count,
            )
