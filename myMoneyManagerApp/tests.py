import datetime
import json

from django.test import TestCase, Client
from django.urls import reverse

from myMoneyManagerApp.models import User, Transaction, Group, Budget


# Create your tests here.
class TestRegistration(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration_success(self):
        data = {
            "username": "testuser",
            "password": "testpass",
            "confirm_password": "testpass",
            "email": "testuser@example.com"
        }

        response = self.client.post(reverse('myMoneyManager:register'), data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(email="testuser@example.com").first().email, 'testuser@example.com')


class UserLoginTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass',
            status=0,
            role=1,
            totalExpenses=0
        )

    def test_user_login(self):
        url = reverse('myMoneyManager:user_login')
        data = {'email': 'testuser@example.com', 'password': 'testpass'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'success')
        # self.assertContains(response, 'result')
        # self.assertNotContains(response, 'error')


class UserLogoutTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('myMoneyManager:user_logout')

    def test_user_logout_success(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})


class TransactionTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.transaction = Transaction.objects.create(
            ownerId="user123",
            values=100,
            category=1,
            createTime=datetime.datetime.now(),
            transactionType=1,
            description="test transaction"
        )
        self.add_transaction_url = reverse('myMoneyManager:add_single_transaction')
        self.edit_transaction_url = reverse('myMoneyManager:edit_single_transaction')
        self.delete_transaction_url = reverse('myMoneyManager:delete_single_transaction')
        self.search_transactions_self_url = reverse('myMoneyManager:search_transactions')
        self.search_transactions_group_url = reverse('myMoneyManager:search_transactions_group')
        self.group = Group.objects.create(
            name='testgroup',
            adminId=1,
            billList='1;',
            numMembers=1,
            memberIds='1;',
            email_list='test@test'

        )
    def test_get_transaction_list_self(self):
        response = self.client.get(reverse('myMoneyManager:transaction'))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, self.transaction.ownerId)
        # self.assertContains(response, self.transaction.description)

    def test_get_transaction_list_group(self):
        response = self.client.get(reverse('myMoneyManager:transaction_group'), {'userId': 'user123'})
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, self.transaction.ownerId)
        # self.assertContains(response, self.transaction.description)

    # def test_add_single_transaction_self(self):
    #     data = {
    #         'ownerId': 'user123',
    #         'values': 200,
    #         'category': 1,
    #         'createTime': datetime.datetime.now(),
    #         'description': 'new test transaction'
    #     }
    #     response = self.client.post(reverse('myMoneyManager:add_single_transaction'), data=json.dumps(data),
    #                                 content_type='application/json')
    #     self.assertEqual(response.status_code, 200)  # expecting a redirect after successful POST request
        # self.assertTrue(Transaction.objects.filter(description='new test transaction').exists())

    def test_add_single_transaction_group(self):
        response = self.client.post(self.add_transaction_url, json.dumps({
            'userId': 1,
            'groupId': 2,
            'category': 1,
            'values': 10.0,
            'description': 'Bought some groceries'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_edit_single_transaction(self):
        response = self.client.post(self.edit_transaction_url, json.dumps({
            'transactionId': self.transaction.transactionId,
            'category': 1,
            'values': 50.0,
            'description': 'Train tickets'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_single_transaction(self):
        response = self.client.post(self.delete_transaction_url, json.dumps({
            'transactionId': self.transaction.transactionId
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_search_transactions_self(self):
        response = self.client.get(f"{self.search_transactions_self_url}?q=Food")
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('list' in json.loads(response.content))

    def test_search_transactions_group(self):
        response = self.client.get(f"{self.search_transactions_group_url}?q=Travel&groupId={self.group.groupId}")
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('list' in json.loads(response.content))


class TestSetBudget(TestCase):
    def setUp(self):
        self.client = Client()

    def test_set_budget_success(self):
        # Create a test user and budget object for the user
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass',
            status=0,
            role=1,
            totalExpenses=0
        )
        budget = Budget.objects.create(ownerId=user.userId, setBudget=0,
                                       startDate=datetime.datetime.now(),
                                       modifyTime=datetime.datetime.now())

        # Prepare test data
        data = {
            'userId': user.userId,
            'setBudget': 1000
        }

        # Make the POST request to the view
        response = self.client.post(reverse('myMoneyManager:set_budget'), data=json.dumps(data),
                                    content_type='application/json')

        # Check if the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], 'Budget set successfully')

        # Check if the budget object has been updated
        budget.refresh_from_db()
        self.assertEqual(budget.setBudget, 1000)


class GroupTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='testpass',
            status=0,
            role=1,
            totalExpenses=0,
        )
        self.newuser = User.objects.create(
            username='newuser',
            email='newuser@example.com',
            password='newpass',
            status=0,
            role=1,
            totalExpenses=0
        )
        self.group = Group.objects.create(name='testgroup', adminId=self.user.userId,
                                          billList='', numMembers=1, memberIds=str(self.user.userId) + ';',
                                          email_list=str(self.user.email) + ';')
        self.user.groupId = str(self.group.groupId) + ';'
        self.user.save()

    def test_create_group(self):
        response = self.client.post(reverse('myMoneyManager:create_group'),
                                    data=json.dumps({'name': 'newgroup', 'userId': self.user.userId}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('groupId' in json.loads(response.content))

    def test_add_member(self):
        response = self.client.post(reverse('myMoneyManager:add_member'),
                                    data=json.dumps({'groupId': self.group.groupId, 'email': self.newuser.email,
                                                     'userId': self.user.userId}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(self.group.memberIds, str(self.user.userId) + ';' + str(self.newuser.userId) + ';')
        # self.assertEqual(self.group.numMembers, 2)
        # self.assertEqual(self.newuser.groupId, str(self.group.groupId) + ';')

    def test_delete_group(self):
        response = self.client.post(reverse('myMoneyManager:delete_group'),
                                    data=json.dumps({'groupId': self.group.groupId, 'userId': self.user.userId}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # self.assertFalse(Group.objects.filter(groupId=self.group.groupId).exists())
        # self.assertEqual(self.user.groupId, )

    def test_remove_member(self):
        self.group.memberIds += str(self.newuser.userId) + ';'
        self.group.numMembers += 1
        self.group.email_list += self.newuser.email + ';'
        self.group.save()
        self.newuser.groupId = str(self.group.groupId) + ';'
        self.newuser.save()
        response = self.client.post(reverse('myMoneyManager:remove_member'),
                                    data=json.dumps({'groupId': self.group.groupId, 'email': self.newuser.email,
                                                     'userId': self.user.userId}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(self.group.memberIds, str(self.user.userId) + ';')
        # self.assertEqual(self.group.numMembers, 1)
        # self.assertEqual(self.newuser.groupId, '')

    def tearDown(self):
        self.user.delete()
        self.group.delete()
