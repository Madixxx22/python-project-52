from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from task_manager.tasks.models import Tasks

from task_manager.utils import get_test_data
from task_manager.users.models import CustomUser


# Create your tests here.
class TestTasks(TestCase):
    fixtures = ['tasks.json', 'users.json', 'statuses.json']

    @classmethod
    def setUpTestData(cls):
        user_data = get_test_data('test_user.json')
        exist_user_data = user_data['existing']
        cls.user = CustomUser.objects.get(username=exist_user_data['username'])
        cls.test_data = get_test_data('test_task.json')

    def assertTasks(self, task, task_data):
        self.assertEqual(task.name, task_data['name'])
        self.assertEqual(task.description, task_data['description'])
        self.assertEqual(task.status.pk, task_data['status'])
        self.assertEqual(task.executor.pk, task_data['executor']),

    def test_show_tasks(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tasks:show_tasks'))
        self.assertEqual(response.status_code, 200)

    def test_create_tasks(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tasks:create_task'))
        self.assertEqual(response.status_code, 200)

        create_success = self.test_data['create_success']
        response = self.client.post(
            reverse('tasks:create_task'),
            create_success,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        created_task = Tasks.objects.get(
            name=create_success['name']
        )
        self.assertTasks(created_task, create_success)

    def test_update_views(self):
        self.client.force_login(self.user)
        exist_task_data = self.test_data['existing']
        exist_task = Tasks.objects.get(
            name=exist_task_data['name']
        )
        response = self.client.get(
            reverse('tasks:edit_task', args=[exist_task.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        self.client.force_login(self.user)
        exist_task_data = self.test_data['existing']
        new_task_data = self.test_data['new']
        exist_task = Tasks.objects.get(name=exist_task_data['name'])
        response = self.client.post(
            reverse('tasks:edit_task', args=[exist_task.pk]),
            new_task_data,
            follow=True
        )
        self.assertRedirects(response, reverse('tasks:show_tasks'))
        updated_status = Tasks.objects.get(
            name=new_task_data['name']
        )
        self.assertTasks(updated_status, new_task_data)

    def test_delete_view(self):
        self.client.force_login(self.user)
        exist_task_data = self.test_data['existing']
        task = Tasks.objects.get(name=exist_task_data['name'])
        response = self.client.get(
            reverse('tasks:delete_task', args=[task.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        self.client.force_login(self.user)
        exist_task_data = self.test_data['existing']
        task = Tasks.objects.get(name=exist_task_data['name'])
        response = self.client.post(
            reverse('tasks:delete_task', args=[task.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('tasks:show_tasks'))
        with self.assertRaises(ObjectDoesNotExist):
            Tasks.objects.get(name=exist_task_data['name'])
