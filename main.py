from winrt.windows.ui.notifications.management import UserNotificationListener
from winrt.windows.ui.notifications import NotificationKinds
import asyncio
import time
import event_notifier
from dotenv import load_dotenv

load_dotenv()

def handle_notification(notification):
    if notification.app_info.app_user_model_id == "com.squirrel.Discord.Discord":
        notification_texts = list(map(lambda x: x.text, notification.notification.visual.bindings[0].get_text_elements()))
        event_notifier.send_notification(notification_texts)


async def listen():
    # ask windows how many notifications there are currently
    while True:
        listener = UserNotificationListener.get_current()
        notifications = await listener.get_notifications_async(NotificationKinds.TOAST)
        if len(notifications) > 0:
            for notification in notifications:
                handle_notification(notification)
        time.sleep(1)

asyncio.run(listen())
