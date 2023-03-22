from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Statuses
from task_manager.users.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist

from task_manager.utils import get_test_data


# Create your tests here.
class TestStatuses(TestCase):
    fixtures = ['statuses.json', 'users.json']

    @classmethod
    def setUpTestData(cls):
        user_data = get_test_data('test_user.json')
        exist_user_data = user_data['existing']
        cls.user = CustomUser.objects.get(username=exist_user_data['username'])
        cls.test_data = get_test_data('test_status.json')

    def assertStatus(self, status, status_data):
        self.assertEqual(status.name, status_data['name'])
        self.assertEqual(
            status.created_date.__str__(),
            status_data['created_date']
        )

    def test_show_statuses(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses:show_statuses'))
        self.assertEqual(response.status_code, 200)

    def test_create_status(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses:create_status'))
        self.assertEqual(response.status_code, 200)

        create_success = self.test_data['create_success']
        response = self.client.post(
            reverse('statuses:create_status'),
            create_success,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        created_status = Statuses.objects.get(
            name=create_success['name']
        )
        self.assertStatus(created_status, create_success)

    def test_update_views(self):
        self.client.force_login(self.user)
        exist_status_data = self.test_data['existing']
        exist_status = Statuses.objects.get(
            name=exist_status_data['name']
        )
        response = self.client.get(
            reverse('statuses:edit_status', args=[exist_status.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        self.client.force_login(self.user)
        exist_status_data = self.test_data['existing']
        new_status_data = self.test_data['new']
        exist_status = Statuses.objects.get(name=exist_status_data['name'])
        response = self.client.post(
            reverse('statuses:edit_status', args=[exist_status.pk]),
            new_status_data,
            follow=True
        )
        self.assertRedirects(response, reverse('statuses:show_statuses'))
        updated_status = Statuses.objects.get(
            name=new_status_data['name']
        )
        self.assertStatus(updated_status, new_status_data)

    def test_delete_view(self):
        self.client.force_login(self.user)
        exist_status_data = self.test_data['existing']
        status = Statuses.objects.get(name=exist_status_data['name'])
        response = self.client.get(
            reverse('statuses:delete_status', args=[status.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        self.client.force_login(self.user)
        exist_status_data = self.test_data['existing']
        status = Statuses.objects.get(name=exist_status_data['name'])
        response = self.client.post(
            reverse('statuses:delete_status', args=[status.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('statuses:show_statuses'))
        with self.assertRaises(ObjectDoesNotExist):
            Statuses.objects.get(name=exist_status_data['name'])
