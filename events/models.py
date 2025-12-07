from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    """
    Модель події згідно з ТЗ
    """
    title = models.CharField(max_length=255, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")
    date = models.DateTimeField(verbose_name="Дата проведення")
    location = models.CharField(max_length=255, verbose_name="Локація")

    # Організатор, зв'язок з користувачем (User).
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_events',
        verbose_name="Організатор"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        verbose_name = "Подія"
        verbose_name_plural = "Події"


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
        verbose_name = "Реєстрація"
        verbose_name_plural = "Реєстрації"

    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"