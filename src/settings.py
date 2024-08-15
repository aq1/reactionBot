import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_FILE = os.environ["DATABASE_FILE"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
ADMIN_CHAT_ID = int(os.environ["ADMIN_CHAT_ID"])
RELEASE = os.environ["REACTION_BOT_RELEASE"]
