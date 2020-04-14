from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
import ipdb
from todolist_app.models import ToDo, Priority


class LogTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()

    def test_login(self):
        client = Client()
        response = client.post('/accounts/login/', {'username': 'testuser', 'password': '12345'})
        response = client.get('/')
        self.assertTrue(response.context['user'].is_authenticated)
        # ipdb.set_trace()

    def test_logout(self):
        c = Client()
        response = c.post('/accounts/login/', {'username': 'testuser', 'password': '12345'})
        response = c.get('/')

        response = c.post('/accounts/logout/')
        response = c.get('/')
        self.assertTrue(response.status_code , 302)

    def test_incorrect_login(self):
        c = Client()
        response = c.post('/accounts/login/', {'username': 'testuser', 'password': '1235678'})
        response = c.get('/')
        self.assertTrue(response.status_code, 302)

    def test_incorrect_login_by_forgetting_password(self):
        c = Client()
        response = c.post('/accounts/login/', {'username': 'testuser', 'password': ''})
        response = c.get('/')
        self.assertTrue(response.status_code , 302)


class ViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()

        self.user_2 = User.objects.create(username='testuser2')
        self.user_2.set_password('12345')
        self.user_2.save()

    def test_view_list(self):
        todo = ToDo.objects.create(
            title='Tarea',
            description='tarea',
            done=False,
            priority=Priority.objects.create(name='alta', orders=1),
            created_by=self.user,
            updated_by=self.user,
            asigned_user=self.user,
        )
        client = Client()
        client.force_login(self.user)
        response = client.get('/')
        self.assertEqual(response.context['object_list'][0].id, todo.id)

    def test_view_nothing_list(self):
        client = Client()
        client.force_login(self.user)
        response = client.get('/')
        self.assertEqual(len(response.context['object_list']), 0)

    def test_view_my_list(self):
        todo = ToDo.objects.create(
            title='Tarea 1',
            description='tarea 1',
            done=False,
            priority=Priority.objects.create(name='alta', orders=1),
            created_by=self.user,
            updated_by=self.user,
            asigned_user=self.user,
        )

        todo_2 = ToDo.objects.create(
            title='Tarea 1',
            description='tarea 1',
            done=False,
            priority=Priority.objects.create(name='alta', orders=1),
            created_by=self.user_2,
            updated_by=self.user_2,
            asigned_user=self.user_2,
        )

        client = Client()
        client.force_login(self.user)
        response = client.get('/')

        for issue in response.context['object_list']:
            self.assertEqual(issue.asigned_user, self.user)


class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()

        self.user_2 = User.objects.create(username='testuser2')
        self.user_2.set_password('12345')
        self.user_2.save()

        priority = Priority.objects.create(name='alta', orders=1)
        self.form_data = {
            'title': 'Tarea 1',
            'description': 'tarea 1',
            'done': False,
            'priority': priority.id,
            'created_by': self.user.id,
            'updated_by': self.user.id,
            'asigned_user': self.user.id,
        }
        self.todo = ToDo.objects.create(
            title='Tarea 1',
            description='tarea 1',
            done=False,
            priority=Priority.objects.create(name='alta', orders=1),
            created_by=self.user,
            updated_by=self.user,
            asigned_user=self.user,
        )

    def test_create_todo(self):
        todos_in_database = len(ToDo.objects.all())
        client = Client()
        client.force_login(self.user)
        response = client.post('/create/', self.form_data)
        todo_id = max(ToDo.objects.all().values_list("id"))[0]
        self.assertRedirects(response, f'/view/{todo_id}')
        self.assertEqual(len(ToDo.objects.all()), todos_in_database + 1)

    def test_update_todo(self):
        priority = Priority.objects.create(name='alta', orders=1)
        todos_in_database = len(ToDo.objects.all())
        client = Client()
        client.force_login(self.user)
        todo_id = max(ToDo.objects.filter(asigned_user=self.user).values_list("id"))[0]
        response = client.post(f'/update/{todo_id}', self.form_data)
        # ipdb.set_trace()
        self.assertRedirects(response, '/')
        self.assertEqual(len(ToDo.objects.all()), todos_in_database)

    def test_todo_view_create(self):
        todo_2 = ToDo.objects.create(
            title='Tarea 1',
            description='tarea 1',
            done=False,
            priority=Priority.objects.create(name='alta', orders=1),
            created_by=self.user_2,
            updated_by=self.user_2,
            asigned_user=self.user_2,
        )
        client = Client()
        client.force_login(self.user)
        response = client.get(f'/view/{self.todo.id}')
        self.assertEqual(response.status_code, 200)
        response = client.get(f'/view/{todo_2.id}')
        self.assertEqual(response.status_code, 403)

    def test_todo_delete(self):
        client = Client()
        client.force_login(self.user)
        todos_in_database = len(ToDo.objects.all())
        response = client.post(f'/delete/{self.todo.id}')
        self.assertEqual(len(ToDo.objects.all()), todos_in_database - 1)