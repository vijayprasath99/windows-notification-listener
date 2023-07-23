import os

from winrt.windows.ui.notifications.management import UserNotificationListener
from winrt.windows.ui.notifications import NotificationKinds
import asyncio
import time
import discord_client
import logging

discord_message_ignore_sub_str_list = os.getenv("DISCORD_MESSAGE_IGNORE_SUB_STRS").split(",")


def should_ignore_message(mess):
    return any(map(mess.__contains__, discord_message_ignore_sub_str_list))


def handle_notification(notification):
    if notification.app_info.app_user_model_id != "com.squirrel.Discord.Discord":
        return

    logging.info(f'Processing Discord notification')
    notification_texts = list(map(lambda x: x.text, notification.notification.visual.bindings[0].get_text_elements()))
    mess = "::".join(notification_texts)

    if should_ignore_message(mess):
        logging.debug(f'Ignoring discord message: {mess}')
        return

    discord_client.notify_user(notification_texts)


async def listen():
    logging.info("Started Listening to windows notifications")
    while True:
        listener = UserNotificationListener.get_current()
        notifications = await listener.get_notifications_async(NotificationKinds.TOAST)
        if len(notifications) > 0:
            logging.debug(f'Retrieved windows {len(notifications)} notifications')
            for notification in notifications:
                handle_notification(notification)
        time.sleep(1)

asyncio.run(listen())
