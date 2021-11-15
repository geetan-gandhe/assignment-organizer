from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from organizer.models import Class,Notes
from django.core.files import File
from django.urls import reverse
from organizer.views import ClassListView, loginPage, home
from django.contrib.auth.models import AnonymousUser, User

#from oauth2 import Client

import mock


class LoginTest(TestCase):
    def setUp(self):
        User = get_user_model()
        test_user = User.objects.create(username='tester')
        test_user.set_password('a-27')
        test_user.save()
        return test_user

    def test_validate_correct(self):
        c = Client()
        correct_user = c.login(username ='tester', password = 'a-27')
        self.assertTrue(correct_user)

    def test_isAnonymous(self):
        c = Client()
        c.login(username='tester', password='a-27')
        User = get_user_model()
        user = User.objects.get(username='tester')
        self.assertFalse(user.is_anonymous)

    def test_validate_logout(self):
        c = Client()
        c.login(username ='tester', password = 'a-27')
        User = get_user_model()
        user = User.objects.get(username = 'tester')
        #self.assertFalse(user.is_anonymous)
        c.logout()
        self.assertTrue(user.is_authenticated)


#test_models
class ClassTest(TestCase):
    @classmethod
    def setUp(cls):
        Class.objects.create(class_name='CS2110')

    def test_className(self):
        test_class = Class.objects.create(class_name='CS2110')
        class_name_test = test_class.__str__()
        #print(class_name_test)
        self.assertEqual(class_name_test,'CS2110')

    def test_class_name_max_length(self):
        test_class = Class.objects.create(class_name='CS2110')
        max_length = test_class._meta.get_field('class_name').max_length
        #print(max_length)
        self.assertEqual(max_length,100)

    def test_class_users_name(self):
        test_class = Class.objects.create(class_name='CS2110')
        username_test = test_class._meta.get_field('users').verbose_name
        self.assertEqual(username_test,'users')

class NoteTest(TestCase):
    @classmethod
    def setUp(cls):
        Class.objects.create(class_name='CS2110')

    def test_note_create(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'test.pdf'
        file_model = Notes(file=file_mock)
        class_test = Class.objects.create(class_name='BME4995')
        class_test.save()
        note = Notes(file=file_model,course=class_test)
        note_test = note.file.__str__()
        self.assertEqual(note_test,'test.pdf')

#view test
class ClassListViewTest(TestCase):
    @classmethod
    def setUp(cls):
        User = get_user_model()
        test_user = User.objects.create(username='tester')
        test_user.set_password('a-27')
        test_user.save()
        return test_user
        number_of_classes = 30
        for class_id in range(number_of_classes):
            Class.objects.create(class_name="CS2110{class_id}")

    def test_environment_set_in_context(self):
        self.factory = RequestFactory()
        User = get_user_model()
        self.user = User.objects.get(id=1)
        request = self.factory.get('organizer/home')
        request.user = self.user
        request.user = AnonymousUser()
        # Test my_view() as if it were deployed at /customer/details
        response = home(request)
        self.assertEqual(response.status_code, 200)
        # Use this syntax for class-based views.

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/organizer/classes')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('organizer:classes'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('organizer:classes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organizer/classes.html')

