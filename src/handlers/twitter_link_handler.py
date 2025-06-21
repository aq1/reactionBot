from urllib.parse import urlparse

from telegram import Update


async def twitter_link_handler(update: Update, _):
    if not update.effective_message:
        return
    if not update.effective_message.text:
        return
    links = []
    for entity in update.effective_message.entities:
        if entity.type not in [entity.URL, entity.TEXT_LINK]:
            continue
        link = update.effective_message.text[entity.offset:entity.offset + entity.length]
        parsed_link = urlparse(link)
        if parsed_link.hostname != "x.com":
            continue
        links.append(f"https://fixupx.com{parsed_link.path}")

    if not links:
        return
    await update.effective_message.reply_text("\n".join(links))

