from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Test class for task creation
class TaskCreationTest(APITestCase):
    def setUp(self):
        # Creating a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.url = reverse('task-list-create')

    def test_create_task_successful(self):
        # Test case for successful task creation
        data = {
            'title': 'Test Task',
            'description': 'This is a test task',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['completed'], False)

    def test_create_task_without_title(self):
        # Test case for missing title field
        data = {
            'description': 'This is a test task without title',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('title', response.data)

    def test_create_task_unauthenticated(self):
        # Test case for unauthenticated request
        self.client.logout()
        data = {
            'title': 'Test Task Unauthenticated',
            'description': 'This task is created without authentication',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 401)
