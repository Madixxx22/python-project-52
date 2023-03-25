from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from task_manager.users.models import CustomUser
from task_manager.utils import get_test_data


class TestDataBase(TestCase):
    path_test_data = ""

    def setUp(self) -> None:
        self.test_data = get_test_data(self.path_test_data)
        user_data = get_test_data('test_user.json')
        exist_user_data = user_data['existing']
        self.user = CustomUser.objects.get(
            username=exist_user_data['username']
        )
        self.client.force_login(self.user)


class TestBase():
    model = None
    show_url = ""
    create_url = ""
    edit_url = ""
    delete_url = ""

    def test_show(self) -> None:
        response = self.client.get(reverse_lazy(self.show_url))
        self.assertEqual(response.status_code, 200)

    def test_create(self) -> None:
        response = self.client.get(reverse_lazy(self.create_url))
        self.assertEqual(response.status_code, 200)

        create_success = self.test_data['create_success']
        response = self.client.post(
            reverse_lazy(self.create_url),
            create_success,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        created_item = self.model.objects.get(
            pk=create_success['pk']
        )
        self.assertItem(created_item, create_success)

    def test_update_views(self) -> None:
        exist_item_data = self.test_data['existing']
        exist_item = self.model.objects.get(
            pk=exist_item_data['pk']
        )
        response = self.client.get(
            reverse_lazy(self.edit_url, args=[exist_item.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_update(self) -> None:
        exist_item_data = self.test_data['existing']
        new_item_data = self.test_data['new']
        exist_item = self.model.objects.get(pk=exist_item_data['pk'])
        response = self.client.post(
            reverse_lazy(self.edit_url, args=[exist_item.pk]),
            new_item_data,
            follow=True
        )
        self.assertRedirects(response, reverse_lazy(self.show_url))
        updated_status = self.model.objects.get(
            pk=new_item_data['pk']
        )
        self.assertItem(updated_status, new_item_data)

    def test_delete_view(self) -> None:
        exist_item_data = self.test_data['existing']
        item = self.model.objects.get(pk=exist_item_data['pk'])
        response = self.client.get(
            reverse_lazy(self.delete_url, args=[item.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_delete(self) -> None:
        exist_item_data = self.test_data['existing']
        item = self.model.objects.get(pk=exist_item_data['pk'])
        response = self.client.post(
            reverse_lazy(self.delete_url, args=[item.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse_lazy(self.show_url))
        with self.assertRaises(ObjectDoesNotExist):
            self.model.objects.get(pk=exist_item_data['pk'])


class TestIndex(TestCase):

    def test_home_page(self) -> None:
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)


class TestLogin(TestCase):

    def create_custom_user(self) -> None:
        self.data_user = {
                    'username': 'test',
                    'password': '123456789'
                }
        self.user = CustomUser.objects.create_user(**self.data_user)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

    def test_login(self):
        self.create_custom_user()
        response = self.client.post(
            reverse('login'),
            self.data_user,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('homepage'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self) -> None:
        response = self.client.post(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
