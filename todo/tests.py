from django.test import TestCase
from todo.models import Todo
from django.contrib.auth.models import User

class TodoTestCase(TestCase):
    def setUp(self):
        myuser = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        myuser2 = User.objects.create_user('johnny', 'lennons@thebeatles.com', 'johnnypassword')
        
        Todo.objects.create(title = 'Walk the dog', memo = 'before noon', important = True, user = myuser)
        Todo.objects.create(title = 'Get pizza', important = True, user = myuser)
        Todo.objects.create(title = 'Cook', memo = 'pasta', important = False, user = myuser)
        Todo.objects.create(title = 'Read a book', important = True, user = myuser2)
        Todo.objects.create(title = 'Run', memo = 'in the morning', important = False, user = myuser2)
        Todo.objects.create(title = 'Buy milk', memo = 'in the afternoon', important = False, user = myuser2)

    def test_todo_important(self):
        """Todos are correctly identified as important"""

        walk = Todo.objects.get(title = 'Walk the dog')
        get = Todo.objects.get(title = 'Get pizza')
        cook = Todo.objects.get(title = 'Cook')
        read = Todo.objects.get(title = 'Read a book')
        run = Todo.objects.get(title = 'Run')
        buy = Todo.objects.get(title = 'Buy milk')
        
        self.assertTrue(walk.important)
        self.assertTrue(get.important)
        self.assertFalse(cook.important)
        self.assertTrue(read.important)
        self.assertFalse(run.important)
        self.assertFalse(buy.important)

    def test_todo_memo(self):
        """Todos are correctly identified as having memo"""

        walk = Todo.objects.get(title = 'Walk the dog')
        get = Todo.objects.get(title = 'Get pizza')
        cook = Todo.objects.get(title = 'Cook')
        read = Todo.objects.get(title = 'Read a book')
        run = Todo.objects.get(title = 'Run')
        buy = Todo.objects.get(title = 'Buy milk')

        self.assertEqual(walk.memo, 'before noon')
        self.assertEqual(get.memo,'')
        self.assertEqual(cook.memo, 'pasta')
        self.assertEqual(read.memo,'')
        self.assertEqual(run.memo, 'in the morning')
        self.assertEqual(buy.memo,'in the afternoon')

    def test_todo_user(self):
        """If the user is correctly identified"""

        walk = Todo.objects.get(title = 'Walk the dog')
        get = Todo.objects.get(title = 'Get pizza')
        cook = Todo.objects.get(title = 'Cook')
        read = Todo.objects.get(title = 'Read a book')
        run = Todo.objects.get(title = 'Run')
        buy = Todo.objects.get(title = 'Buy milk')

        self.assertEqual(walk.user.username, 'john')
        self.assertEqual(get.user.username, 'john')
        self.assertEqual(cook.user.username, 'john')
        self.assertEqual(read.user.username, 'johnny')
        self.assertEqual(run.user.username, 'johnny')
        self.assertEqual(buy.user.username, 'johnny')

    def test_todo_user_count(self):
        """If the otdos are correcty associated with the users"""
        jtodos = Todo.objects.filter(user = 1).count()
        jytodos = Todo.objects.filter(user = 2).count()

        self.assertEqual(jtodos, 3)
        self.assertEqual(jytodos, 3)
