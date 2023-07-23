import os
from discord import SyncWebhook
from dotenv import load_dotenv
import logging

load_dotenv()

webhook = SyncWebhook.from_url(os.getenv("DISCORD_WEBHOOK_URL"))

def notify_user(message):
    logging.debug(f'Sending message {message} to discord webhoot url')
    webhook.send(message)
