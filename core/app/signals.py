from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import SinglePage, TelegramSetting, TelegramLog
from .utils import send_telegram_photo, send_telegram_message
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=SinglePage)
def send_post_to_telegram(sender, instance, created, **kwargs):
    if instance.status != 'published':
        return
    
    should_send = False
    
    if created and instance.status == 'published':
        should_send = True
    else:
        existing_log = TelegramLog.objects.filter(news=instance, status='sent').exists()
        if not existing_log:
            should_send = True
    
    if not should_send:
        return
    
    telegram_setting = TelegramSetting.objects.filter(is_active=True).first()
    if not telegram_setting:
        print("❌ No active Telegram settings found in database")
        return
    
    if telegram_setting.test_mode:
        print("🧪 Test mode enabled - not sending to actual Telegram")
        return
    
    print(f"🔔 Telegram signal triggered for: {instance.title}")
    
    if telegram_setting.post_format:
        message = telegram_setting.post_format.format(
            title=instance.title,
            category=instance.category.name if instance.category else 'General',
            description=instance.description[:200] + '...' if len(instance.description) > 200 else instance.description,
            link=f"{settings.SITE_URL}/single/{instance.id}/"
        )
    else:
        message = (
            f"🔔 YANGI YANGILIK!\n\n"
            f"<b>{instance.title}</b>\n\n"
        )
        
        if instance.category:
            message += f"🏷 <b>Kategoriya:</b> {instance.category.name}\n\n"
        
        if instance.description:
            short_desc = instance.description[:200]
            if len(instance.description) > 200:
                short_desc += '...'
            message += f"{short_desc}\n\n"
        
        message += f"🔗 <a href='{settings.SITE_URL}/single/{instance.id}/'>Batafsil o'qish</a>"
    
    try:
        if instance.image and instance.image.url:
            image_url = f"{settings.SITE_URL}{instance.image.url}"
            print(f"📸 Sending photo: {image_url}")
            result = send_telegram_photo(image_url, message)
        else:
            print(f"📝 Sending text message")
            result = send_telegram_message(message)
        
        TelegramLog.objects.create(
            news=instance,
            channel_id=telegram_setting.channel_id,
            status='sent',
            telegram_message_id=str(result.get('message_id', '')) if isinstance(result, dict) else ''
        )
        print("✅ Telegram message sent and logged")
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Failed to send Telegram message: {error_msg}")
        
        TelegramLog.objects.create(
            news=instance,
            channel_id=telegram_setting.channel_id,
            status='error',
            error_message=error_msg
        )