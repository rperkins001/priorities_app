from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Todo

class TodoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.todo = Todo.objects.create(
            title='Test todo',
            user=self.user
        )

    def test_todo_list(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test todo')

    def test_create_todo(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'New todo',
            'description': 'A new todo',
        }
        response = self.client.post(reverse('create_todo'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Todo.objects.filter(title='New todo').exists())

    def test_delete_todo(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('delete_todo', args=[self.todo.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(title='Test todo').exists())