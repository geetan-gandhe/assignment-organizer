from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from organizer.models import Class,Notes, Reviews, Category, TodoList
from django.core.files import File
from django.urls import reverse
from organizer.views import ClassListView

import mock


class LoginTest(TestCase):
    def setUp(self):
        User = get_user_model()
        test_user = User.objects.create(username='tester')
        test_user.set_password('a-27')
        test_user.save()

    def test_validate_correct(self):
        c = Client()
        correct_user = c.login(username ='tester', password = 'a-27')
        self.assertTrue(correct_user)

    def test_validate_logout(self):
        c = Client()
        c.login(username ='tester', password = 'a-27')
        User = get_user_model()
        user = User.objects.get(username = 'tester')
        self.assertFalse(user.is_anonymous)
        #c.logout()
        #self.assertTrue(user.is_authenticated)

#test_models
class ClassTest(TestCase):
    @classmethod
    def setUp(cls):
        Class.objects.create(class_name='CS2110')

    def test_className(self):
        test_class = Class.objects.get(id=1)
        class_name_test = test_class.__str__()
        #print(class_name_test)
        self.assertEqual(class_name_test,'CS2110')

    def test_max_length(self):
        test_class = Class.objects.create(class_name='CS2110')
        max_length = test_class._meta.get_field('class_name').max_length
        #print(max_length)
        self.assertEqual(max_length,100)

class NoteTest(TestCase):
    def test_note_create(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'test.pdf'
        file_model = Notes(file=file_mock)
        class_test = Class.objects.create(class_name='BME4995')
        class_test.save()
        note = Notes(file=file_model,course=class_test)
        note_test = note.file.__str__()
        self.assertEqual(note_test,'test.pdf')

class ReviewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_review_create_working(self):
        Reviews.objects.create(class_Instructor='Horton', review='solid')
        test_review = Reviews.objects.get(class_Instructor='Horton')
        self.assertEqual(test_review.review, 'solid')

    def test_review_create_failing(self):
        Reviews.objects.create(class_Instructor='Horton', review='solid')
        test_review = Reviews.objects.get(class_Instructor='Horton')
        self.assertNotEqual(test_review.review, 'horrid!')

    def test_review_nonempty_review(self):
        test_course = Class.objects.create(class_name='class')
        Reviews.objects.create(class_Instructor='McBurn',
                               review='review',
                               course=test_course)
        test_todo = Reviews.objects.get(review='review')
        self.assertNotEqual(len(test_todo.review), 0)

    def test_review_http(self):
        response = self.client.get('/reviews/')
        self.assertEqual(response.status_code, 200)

    def test_review_max(self):
        test_course = Class.objects.create(class_name='class')
        test_rev = Reviews.objects.create(class_Instructor='bob',
                                          review='review',
                                          course=test_course)
        test_max = test_rev._meta.get_field('class_Instructor').max_length
        self.assertEqual(test_max, 100)

    def test_review_form(self):
        test_course = Class.objects.create(class_name='class')
        data = {'class_Instructor': 'McBurn',
                'review': 'review',
                'course': test_course,
                }
        response = self.client.post('/reviews', data)
        post = response.get('/reviews', data)
        self.assertEqual(post['course'], test_course)

    def test_review_form2(self):
        test_course = Class.objects.create(class_name='class')
        data = {'class_Instructor': 'McBurn',
                'review': 'review',
                'course': test_course,
                }
        response = self.client.post('/reviews', data)
        post = response.get('/reviews', data)
        self.assertEqual(post['class_Instructor'], 'McBurn')

    def test_review_form_success(self):
        test_course = Class.objects.create(class_name='class')
        response = self.client.post('/reviews', {'class_Instructor': 'McBurn',
                                                 'review': 'review',
                                                 'course': test_course,
                                                 })
        self.assertTrue(response.status_code, 200)

    def test_review_form_failure(self):
        test_course = Category.objects.create(name='class')
        response = self.client.post('/reviews', {'class_Instructor': 'McBurn',
                                                 'review': 'review',
                                                 'course': test_course,
                                                 })
        self.assertTrue(response.status_code, 404)


class ToDoTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_todo_create_working(self):
        test_cat = Category.objects.create(name='cat1')
        test_todo = TodoList.objects.create(title='List1', category=test_cat)
        self.assertEqual(test_todo.title, 'List1')

    def test_todo_create_failing(self):
        test_cat = Category.objects.create(name='cat1')
        test_todo = TodoList.objects.create(title='List1', category=test_cat)
        self.assertNotEqual(test_todo.title, 'List2')

    def test_todo_nonempty_title(self):
        test_cat = Category.objects.create(name='cat1')
        TodoList.objects.create(title='title', content='alpha', category=test_cat)
        test_todo = TodoList.objects.get(content='alpha')
        self.assertNotEqual(len(test_todo.title), 0)

    def test_todo_http(self):
        response = self.client.get('/index')
        self.assertEqual(response.status_code, 200)

    def test_todo_max(self):
        test_cat = Category.objects.create(name='cat1')
        test_todo = TodoList.objects.create(title='title',
                                            content='text',
                                            category=test_cat,
                                            created='2020-11-22',
                                            due_date='2020-12-04'
                                            )
        test_max = test_todo._meta.get_field('title').max_length
        self.assertEqual(test_max, 250)

    def test_todo_form1(self):
        test_cat = Category.objects.create(name='cat1')
        data = {'title': 'title',
                'content': 'review',
                'category': test_cat,
                "created": "2020-11-22",
                "due_date": "2020-12-04"
                }
        response = self.client.post('/index', data)
        post = response.get('/index', data)
        self.assertEqual(post['category'], test_cat)

    def test_todo_form2(self):
        test_cat = Category.objects.create(name='cat1')
        data = {'title': 'title',
                'content': 'review',
                'category': test_cat,
                "created": "2020-11-22",
                "due_date": "2020-12-04"
                }
        response = self.client.post('/index', data)
        post = response.get('/index', data)
        self.assertEqual(post['created'], '2020-11-22')

    def test_todo_form_success(self):
        test_cat = Category.objects.create(name='cat1')
        response = self.client.post('/index', {'title': 'test_title',
                                               'content': 'review',
                                               'category': test_cat,
                                               "created": "2020-11-22",
                                               "due_date": "2020-12-04"
                                               })
        self.assertTrue(response.status_code, 200)

    def test_todo_form_failure(self):
        test_cat = Reviews.objects.create(review='cat1')
        response = self.client.post('/index', {'title': 'test_title',
                                               'content': 'review',
                                               'category': test_cat,
                                               "created": "2020-11-22",
                                               "due_date": "2020-12-04"
                                               })
        self.assertTrue(response.status_code, 404)