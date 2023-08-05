from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task

# Test class for task update and delete
class TaskUpdateDeleteTest(APITestCase):
    
    def setUp(self):
        # Creating a test user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.task = Task.objects.create(title='Test Task', description='Description', created_by=self.user)

        self.url_detail = reverse('task-retrieve-update-destroy', kwargs={'pk': self.task.pk})

    def test_update_task(self):
        # Test case for updating a task
        update_data = {'title': 'Updated Task', 'description': 'Updated Description'}
        response = self.client.put(self.url_detail, update_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, update_data['title'])
        self.assertEqual(self.task.description, update_data['description'])

    def test_delete_task(self):
        # Test case for deleting a task
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.task.pk)

    def test_update_task_unauthenticated(self):
        # Test case for unauthenticated update request
        self.client.logout()
        update_data = {'title': 'Updated Task', 'description': 'Updated Description'}
        response = self.client.put(self.url_detail, update_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_delete_task_unauthenticated(self):
        # Test case for unauthenticated delete request
        self.client.logout()
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, 401)
