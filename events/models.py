from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    """
    Модель події згідно з ТЗ
    """
    title = models.CharField(
        max_length=200,
        verbose_name="Title",
        db_index=True
    )

    description = models.TextField(verbose_name="Description")

    date = models.DateTimeField(
        verbose_name="Date and Time",
        db_index=True
    )

    location = models.CharField(
        max_length=100,
        verbose_name="Location",
        db_index=True
    )
    # Організатор, зв'язок з користувачем (User).
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_events',
        verbose_name="Organizer"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
        verbose_name = "Registration"
        verbose_name_plural = "Registrations"

    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"