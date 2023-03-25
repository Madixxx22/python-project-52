from typing import Any
from django.db import models

from task_manager.tests import TestBase, TestDataBase
from task_manager.users.models import CustomUser


# Create your tests here.
class TestUser(TestDataBase, TestBase):
    fixtures = ['users.json']
    model = CustomUser
    path_test_data = "test_user.json"
    show_url = 'users:show_users'
    create_url = 'users:register'
    edit_url = 'users:edit_user'
    delete_url = 'users:delete_user'

    def assertItem(
        self,
        user: models.query.QuerySet[Any],
        user_data: dict
    ) -> None:
        self.assertEqual(user.username, user_data['username'])
        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.last_name, user_data['last_name'])
