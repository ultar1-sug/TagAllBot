"""The main package of TagAll Bot."""

import logging
from os import environ

from telegram.ext import Dispatcher, Updater
from tagall_bot.sql.roles import get_users, sudo_users, tag_users

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
LOGGER = logging.getLogger(__name__)

TOKEN = environ.get("TOKEN", "")
OWNER_ID = int(environ.get("OWNER_ID", ""))
SUDO_USERS = {int(x) for x in environ.get("SUDO_USERS", "").split()}
SUDO_GROUPS = {int(x) for x in environ.get("SUDO_GROUPS", "").split()}
DND_USERS = {int(x) for x in environ.get("DND_USERS", "").split()}
WEBHOOK = bool(environ.get("WEBHOOK", False))
URL = environ.get("URL", "")
API_URL = environ.get("API_URL", "")
PORT = int(environ.get("PORT", 5000))

# Set up Updater and Dispatcher
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# Define roles
sudo_users.update(get_users(sudo_users), SUDO_GROUPS)
tag_users = get_users(tag_users)

# Set up roles
for sudo in sudo_users:
    dispatcher.bot_data.setdefault("sudo_users", set()).add(sudo)
for tag in tag_users:
    dispatcher.bot_data.setdefault("tag_users", set()).add(tag)

# Additional setup for admin
dispatcher.bot_data["owner_id"] = OWNER_ID
dispatcher.bot_data["admins"] = sudo_users

# Additional setup for webhook
if WEBHOOK:
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook(URL + TOKEN)
else:
    updater.start_polling()

# Add any additional handlers or setup as needed
