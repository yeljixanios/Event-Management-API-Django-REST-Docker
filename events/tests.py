from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Event, Registration


class EventTests(APITestCase):
    def setUp(self):
        self.user_admin = User.objects.create_user(username='admin', password='pass')
        self.user_tester = User.objects.create_user(username='tester', password='pass')

        self.event = Event.objects.create(
            title="Python Conf",
            description="Test desc",
            date="2025-10-10 10:00:00+00:00",
            location="Kyiv",
            organizer=self.user_admin
        )
        self.url = '/api/events/'

    def test_list_events(self):
        self.client.force_authenticate(user=self.user_tester)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data['results']), 1)

    def test_create_event(self):
        self.client.force_authenticate(user=self.user_tester)
        data = {
            "title": "New Event",
            "description": "Desc",
            "date": "2025-11-11 12:00:00+00:00",
            "location": "Lviv"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_event = Event.objects.get(title="New Event")
        self.assertEqual(new_event.organizer, self.user_tester)

    def test_delete_other_user_event_permission(self):
        self.client.force_authenticate(user=self.user_tester)
        url_detail = f"{self.url}{self.event.id}/"
        response = self.client.delete(url_detail)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Event.objects.count(), 1)

    def test_update_other_user_event_permission(self):
        self.client.force_authenticate(user=self.user_tester)
        url_detail = f"{self.url}{self.event.id}/"

        data = {"title": "Hacked Title"}
        response = self.client.patch(url_detail, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.event.refresh_from_db()
        self.assertEqual(self.event.title, "Python Conf")


class RegistrationTests(APITestCase):
    def setUp(self):
        self.user_victim = User.objects.create_user(username='victim', email='v@test.com', password='pass')
        self.user_attacker = User.objects.create_user(username='attacker', email='a@test.com', password='pass')

        self.event = Event.objects.create(
            title="Conf", date="2025-01-01 12:00:00+00:00", location="K", organizer=self.user_victim
        )

        self.registration = Registration.objects.create(user=self.user_victim, event=self.event)
        self.url = '/api/registrations/'

    def test_registration_flow(self):
        self.client.force_authenticate(user=self.user_attacker)
        data = {"event": self.event.id}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_double_registration_prevented(self):
        self.client.force_authenticate(user=self.user_victim)
        data = {"event": self.event.id}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_delete_others_registration(self):
        self.client.force_authenticate(user=self.user_attacker)
        url_detail = f"{self.url}{self.registration.id}/"

        response = self.client.delete(url_detail)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Registration.objects.filter(id=self.registration.id).exists())

