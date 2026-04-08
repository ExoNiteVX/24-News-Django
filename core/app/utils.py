import random
import string
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def generate_code():
    alphabet = string.ascii_uppercase
    numbers = string.digits
    return ''.join(random.choices(alphabet + numbers, k=20))


def get_telegram_credentials():
    from .models import TelegramSetting
    setting = TelegramSetting.objects.filter(is_active=True).first()
    if setting:
        return setting.bot_token, setting.channel_id
    return settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID


def send_telegram_message(text):
    bot_token, chat_id = get_telegram_credentials()
    
    if not bot_token or not chat_id:
        print("❌ ERROR: Telegram credentials not configured!")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    print(f"📤 Sending to Telegram: {url[:50]}...")

    try:
        response = requests.post(url, data=data, timeout=10)
        result = response.json()

        if result.get('ok'):
            print(f"✅ Telegram message sent successfully!")
            return result
        else:
            print(f"❌ Telegram API error: {result.get('description')}")
            return result
    except Exception as e:
        print(f"❌ Telegram request failed: {e}")
        return False


def send_telegram_photo(image_url, caption):
    bot_token, chat_id = get_telegram_credentials()
    
    if not bot_token or not chat_id:
        print("❌ ERROR: Telegram credentials not configured!")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

    print(f"📸 Sending photo: {image_url}")

    try:
        if '127.0.0.1' in image_url or 'localhost' in image_url:
            local_path = image_url.replace(settings.SITE_URL, '')
            if local_path.startswith('/'):
                local_path = local_path[1:]

            full_path = settings.BASE_DIR / local_path
            print(f"📁 Local file path: {full_path}")

            if full_path.exists():
                with open(full_path, 'rb') as photo_file:
                    files = {'photo': photo_file}
                    data = {
                        "chat_id": chat_id,
                        "caption": caption,
                        "parse_mode": "HTML",
                    }
                    response = requests.post(url, data=data, files=files, timeout=15)
                    result = response.json()

                    if result.get('ok'):
                        print(f"✅ Telegram photo sent (file upload)!")
                        return result
                    else:
                        print(f"❌ Telegram error: {result.get('description')}")
                        return result
            else:
                print(f"❌ File not found: {full_path}")
                return send_telegram_message(caption)
        else:
            data = {
                "chat_id": chat_id,
                "photo": image_url,
                "caption": caption,
                "parse_mode": "HTML",
            }
            response = requests.post(url, data=data, timeout=15)
            result = response.json()

            if result.get('ok'):
                print(f"✅ Telegram photo sent (URL)!")
                return result
            else:
                print(f"❌ Telegram error: {result.get('description')}")
                return result

    except Exception as e:
        print(f"❌ Telegram request failed: {e}")
        return send_telegram_message(caption)