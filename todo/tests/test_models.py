from django.test import TestCase


from ..models import Todo


class TodoModelTestCase(TestCase):

    def test_str_method_should_return_title(self):
        expected_result = 'una nueva tarea'
        todo = Todo(title=expected_result)

        result = todo.__str__()

        self.assertEqual(expected_result, result)
