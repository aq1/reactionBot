from telegram import Update

import db


async def stats_command(update: Update, _):
    stats = db.execute(
        '''select telegram_user.username, telegram_user.full_name, emoji_id, count
            from stat
            left join telegram_user on telegram_user.id = stat.user_id
            where chat_id = ?
            order by count desc;''',
        (update.effective_chat.id,)
    )

    text = []
    for username, fullname, emoji_id, count in stats:
        text.append(f'{username or fullname} {emoji_id} {count}')

    await update.effective_chat.send_message('\n'.join(text))
