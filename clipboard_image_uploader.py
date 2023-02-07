from datetime import datetime
from time import sleep
from discord_webhook import DiscordWebhook
from windows import is_image_in_clipboard, get_image_from_clipboard, get_pixels_from_image, save_image, show_notification

IMAGE_SAVE_DIRECTORY = 'C:\\Users\\Chino\\Pictures\\'
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz'

old_hash = 0
delay = 1
show_notification('Clipboard Image Uploader is running', 3)
while True:
    sleep(delay)
    try:
        if not is_image_in_clipboard():
            continue
        image = get_image_from_clipboard()
        if image is None:
            continue
        new_hash = hash(tuple(get_pixels_from_image(image)))
        if new_hash == old_hash:
            continue
        old_hash = new_hash
        timestamp = datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
        save_image(image, IMAGE_SAVE_DIRECTORY, timestamp)
        webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)
        with open (IMAGE_SAVE_DIRECTORY + timestamp + '.png', 'rb') as f:
            webhook.add_file(file=f.read(), filename=timestamp + '.png')
        response = webhook.execute()
        show_notification('Image saved and sent to discord', 3)
    except Exception as e:
        show_notification('Error occurred: ' + e.args[0], 3)
