"""
 some bug waiting fix
"""
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
import json

from apps.user.models import User

class AccountApiTests(APITestCase):
    def setUp(self):
        self.path = "/api/account/login"
        self.login_data = {
            "success": {"username": "monkyin", "password": "qweqwe123"},
            "wrong_password": {"username": "beibei", "password": "wrong!"},
        }
        self.login_user = User.objects.get(username="monkyin")

    def test_login_success(self):
        response = self.client.post(self.path, {'username': 'monkyin', 'password': 'qweqwe123'},format='json')
        data = json.loads(response.content)
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK,
                          '登陆接口状态码错误')
        self.assertEquals(data['user'].id, self.login_user.id, '登陆成功接口response错误')
        self.assertIn('id', data['user'], '登陆成功后为返回用户数据')


    def test_login_faild(self):
        response = self.client.post(self.path, self.login_data['wrong_password'],format='json')
        data = response.body
        self.assertEquals(response.status_code,
                          status.HTTP_400_BAD_REQUEST,
                          '密码错误状态码错误: 错误信息: {}'.format(response.content))
        self.assertEquals(data['login'], False, '登陆成功接口response错误')

    def test_login_method(self):
        response = self.client.get(self.path, self.login_data['wrong_password'],format='json')
        self.assertEquals(response.status_code,
                                  status.HTTP_403_FORBIDDEN,
                                  '登陆使用get方法没用返回正确状态码: 错误信息: {}'.format(response.content))