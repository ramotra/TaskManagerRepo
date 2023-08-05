from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task

# Test class for task retrieval
class TaskRetrievalTest(APITestCase):
    def setUp(self):
    # Creating a test user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.task1 = Task.objects.create(title='Test Task 1', description='Description 1', created_by=self.user)
        self.task2 = Task.objects.create(title='Test Task 2', description='Description 2', created_by=self.user)

        self.url_list = reverse('task-list-create')
        self.url_detail = reverse('task-retrieve-update-destroy', kwargs={'pk': self.task1.pk})

    def test_retrieve_all_tasks(self):
        # Test case for retrieving all tasks
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_single_task(self):
        # Test case for retrieving a single task
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.task1.title)
        self.assertEqual(response.data['description'], self.task1.description)

    def test_retrieve_task_unauthenticated(self):
        # Test case for unauthenticated request
        self.client.logout()
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, 401)
