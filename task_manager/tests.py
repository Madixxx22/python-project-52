from django.test import TestCase
from django.urls import reverse

from task_manager.users.models import CustomUser

class TestIndex(TestCase):

    def test_home_page(self):
        response = self.client.get(reverse('homepage'))
        return self.assertEqual(response.status_code, 200)


class TestLogin(TestCase):
    
    def create_custom_user(self):
        self.data_user = {
                    'username': 'test',
                    'password': '123456789'
                }
        self.user = CustomUser.objects.create_user(**self.data_user)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='login.html')

    def test_login(self):
        self.create_custom_user()
        response = self.client.post(reverse('login'), self.data_user, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('homepage'))
        self.assertTrue(response.context['user'].is_authenticated)
    
    def test_logout(self):
        response = self.client.post(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
