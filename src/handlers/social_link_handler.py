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
        if link.hostname in ("twitter.com", "x.com"):
            links.append(f"https://fixupx.com{link.path}")
        if link.hostname in ("www.instagram.com", "instagram.com") and not link.path.startswith("/stories/"):
            links.append(f"https://instagramez.com{link.path}")

    for link in links:
        await update.effective_message.reply_text(link)
        await asyncio.sleep(0.5)

