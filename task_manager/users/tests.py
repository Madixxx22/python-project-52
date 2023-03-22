from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist

from task_manager.utils import get_test_data


# Create your tests here.
class TestUser(TestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data('test_user.json')

    def assertUser(self, user, user_data):
        self.assertEqual(user.username, user_data['username'])
        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.last_name, user_data['last_name'])

    def test_show_user(self):
        response = self.client.get(reverse('users:show_users'))
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)

        create_success = self.test_data['create_success']
        response = self.client.post(
            reverse('users:register'),
            create_success,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        created_user = CustomUser.objects.get(
            username=create_success['username']
        )
        self.assertUser(created_user, create_success)

    def test_update_views(self):
        user = CustomUser.objects.get(pk=3)
        self.client.force_login(user)
        exist_user_data = self.test_data['existing']
        exist_user = CustomUser.objects.get(
            username=exist_user_data['username']
        )
        response = self.client.get(
            reverse('users:edit_user', args=[exist_user.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        exist_user_data = self.test_data['existing']
        new_user_data = self.test_data['new']
        user = CustomUser.objects.get(username=exist_user_data['username'])
        self.client.force_login(user)
        exist_user = CustomUser.objects.get(
            username=exist_user_data['username']
        )
        response = self.client.post(
            reverse('users:edit_user', args=[exist_user.pk]),
            new_user_data,
            follow=True
        )

        self.assertRedirects(response, reverse('users:show_users'))
        updated_user = CustomUser.objects.get(
            username=new_user_data['username']
        )
        self.assertUser(updated_user, new_user_data)

    def test_delete_view(self):
        exist_user_data = self.test_data['existing']
        user = CustomUser.objects.get(username=exist_user_data['username'])
        self.client.force_login(user)
        response = self.client.get(
            reverse('users:delete_user', args=[user.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        exist_user_data = self.test_data['existing']
        user = CustomUser.objects.get(username=exist_user_data['username'])
        self.client.force_login(user)
        response = self.client.post(
            reverse('users:delete_user', args=[user.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('users:show_users'))
        with self.assertRaises(ObjectDoesNotExist):
            CustomUser.objects.get(username=exist_user_data['username'])
