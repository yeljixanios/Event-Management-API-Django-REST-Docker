from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Registration


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class EventSerializer(serializers.ModelSerializer):
    """
    Серіалізатор для подій.
    Використовується для перегляду та створення подій.
    """
    organizer = serializers.ReadOnlyField(source='organizer.username')

    participants_count = serializers.IntegerField(source='participants.count', read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'organizer', 'participants_count', 'created_at']
        read_only_fields = ['organizer', 'created_at']


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Серіалізатор для реєстрації на події.
    """

    class Meta:
        model = Registration
        fields = ['id', 'event', 'user', 'registered_at']
        read_only_fields = ['user', 'registered_at']

    def validate(self, data):
        user = self.context['request'].user
        event = data['event']

        if Registration.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError("Ви вже зареєстровані на цю подію.")

        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

        return user