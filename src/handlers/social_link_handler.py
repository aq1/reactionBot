import asyncio
from urllib.parse import urlparse

from telegram import Update


async def social_link_handler(update: Update, _):
    if not update.effective_message:
        return
    if not update.effective_message.text:
        return
    links = []
    for entity in update.effective_message.entities:
        if entity.type not in [entity.URL, entity.TEXT_LINK]:
            continue
        link = urlparse(update.effective_message.text[entity.offset:entity.offset + entity.length])
        if not link.hostname:
            continue
        if link.hostname == "x.com":
            links.append(f"https://fixupx.com{link.path}")
        if link.hostname.endswith("instagram.com") and link.path.startswith("/p/"):
            links.append(f"https://ddinstagram.com{link.path}?{link.query}".rstrip("?"))

    for link in links:
        await update.effective_message.reply_text(link)
        await asyncio.sleep(0.5)

