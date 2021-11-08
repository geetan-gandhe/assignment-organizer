from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from organizer.models import Class,Notes
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


