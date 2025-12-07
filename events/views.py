from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer, UserRegistrationSerializer
from .permissions import IsOrganizerOrReadOnly

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().select_related('organizer')
    serializer_class = EventSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]

    # --- БОНУС: Фільтрація та Пошук ---
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['date', 'location']  # Фільтр: ?location=Kyiv
    search_fields = ['title', 'description']  # Пошук: ?search=Python
    ordering_fields = ['date', 'created_at']  # Сортування: ?ordering=date

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class RegistrationViewSet(viewsets.ModelViewSet):
    """
    API для реєстрації користувачів на події.
    """
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    http_method_names = ['get', 'post', 'delete', 'head']

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user).select_related('event', 'user')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]