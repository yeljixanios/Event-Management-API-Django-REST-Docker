from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Registration


@receiver(post_save, sender=Registration)
def send_registration_email(sender, instance, created, **kwargs):
    if created:
        user_email = instance.user.email

        if not user_email:
            print(f"⚠️  WARNING: Email notification skipped. User '{instance.user.username}' has no email address.")
            return

        subject = f"Підтвердження реєстрації: {instance.event.title}"
        message = (
            f"Вітаємо, {instance.user.username}!\n\n"
            f"Ви успішно зареєструвалися на подію '{instance.event.title}'.\n"
            f"Дата: {instance.event.date}\n"
            f"Локація: {instance.event.location}\n\n"
            f"Чекаємо на вас!"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
        )