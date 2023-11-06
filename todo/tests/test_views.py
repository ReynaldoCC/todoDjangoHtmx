from http import HTTPStatus
from unittest import TestCase

from django.http import HttpRequest
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from todo.views import ToggleCompleteView, DeleteTodoView, ToggleAllTodoView, RemoveCompletedView


class HostTestCase(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_initial_page_renders_with_title_as_expected(self):
        path = reverse('home')
        url = self.live_server_url + path
        expected_path = reverse('todo_list')
        expected_title = 'ToDo App'
        self.driver.get(url)
        self.assertEqual(expected_title, self.driver.title)
        self.assertIn(expected_path, self.driver.current_url)


class TodoCreateTestCase(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_create_todo_as_expected(self):
        path = reverse('todo_list')
        url = self.live_server_url + path
        self.driver.get(url)

        add_todo_input = self.driver.find_element(By.CLASS_NAME, 'new-todo')
        add_todo_input.send_keys('new tasks to do')
        add_todo_input.send_keys(Keys.RETURN)

        try:
            item_created = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'item-1'))
            )
        except NoSuchElementException as _:
            pass
        else:
            self.assertIsNotNone(item_created)


class TodoUpdateTestCase(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_update_todo_as_expected(self):
        path = reverse('todo_list')
        url = self.live_server_url + path
        self.driver.get(url)
        add_todo_input = self.driver.find_element(By.CLASS_NAME, 'new-todo')
        initial_title = 'new task to do'
        add_todo_input.send_keys(initial_title)
        add_todo_input.send_keys(Keys.RETURN)
        result_text = ''
        added_title = ' later'
        expected_text = initial_title + added_title

        element = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.todo-list li div.view label.title'))
        )
        action = ActionChains(self.driver)
        action.double_click(on_element=element)
        action.perform()
        update_input = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'todo-input'))
        )
        update_input.send_keys(added_title)
        update_input.send_keys(Keys.RETURN)

        updated_item = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.todo-list li div.view label.title'))
        )
        if updated_item:
            result_text = updated_item.get_attribute("textContent")
        self.assertEqual(expected_text.lower(), result_text.lower())


class TodoToggleViewsTestCase(TestCase):

    def setUp(self):
        from todo.models import Todo
        self.view = ToggleCompleteView()
        self.request = HttpRequest()
        self.request.htmx = True
        self.view.request = self.request
        self.todo = Todo.objects.create(title='Test Todo', completed=False)
        self.view.kwargs = {'pk': self.todo.pk}

    def test_view_toggle_completed(self):
        # Arrange

        # Act
        response = self.view.put(self.request)
        self.todo.refresh_from_db()

        # Assert
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(['todo/partials/todo-app.html'], response.template_name)
        self.assertEqual(True, self.todo.completed)


class TodoDeleteViewsTestCase(TestCase):

    def setUp(self):
        from todo.models import Todo
        self.view = DeleteTodoView()
        self.request = HttpRequest()
        self.request.htmx = True
        self.view.request = self.request
        self.todo = Todo.objects.create(title='Test Todo', completed=False)
        self.view.kwargs = {'pk': self.todo.pk}

    def test_delete_todo(self):
        # Arrange

        # Act
        response = self.view.delete(self.request)

        # Assert
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(['todo/partials/todo-app.html'], response.template_name)
        self.assertIn('checked', response.context_data)


class ToggleAllTodoCompleteViewTestCase(TestCase):

    def setUp(self):
        from todo.models import Todo
        self.view = ToggleAllTodoView()
        self.request = HttpRequest()
        self.request.htmx = True
        self.view.request = self.request
        self.todos = Todo.objects.bulk_create([Todo(title='Test Todo', completed=False),
                                               Todo(title='Test Todo 1', completed=True),
                                               Todo(title='Test Todo 2', completed=False), ])

    def test_all_todo_toggled_same_value(self):
        # Arrange
        self.request.POST = {'toggle-all': True}

        # Act
        response = self.view.post(self.request)

        # Assert
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(['todo/partials/todo-list.html'], response.template_name)
        self.assertIn('checked', response.context_data)
        self.assertIn('todos', response.context_data)
        self.assertEqual(response.context_data.get('checked'), len(response.context_data.get('todos')))

    def test_all_todo_toggled_checked_zero_when_toggle_false(self):
        # Arrange
        self.request.POST = {'toggle-all': False}
        expected_checked_zero = 0

        # Act
        response = self.view.post(self.request)

        # Assert
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(['todo/partials/todo-list.html'], response.template_name)
        self.assertIn('checked', response.context_data)
        self.assertIn('todos', response.context_data)
        self.assertEqual(expected_checked_zero, response.context_data.get('checked'))


class ClearTodoCompleteViewTestCase(TestCase):

    def setUp(self):
        from todo.models import Todo
        self.view = RemoveCompletedView()
        self.request = HttpRequest()
        self.request.htmx = True
        self.view.request = self.request
        self.todos = Todo.objects.bulk_create([Todo(title='Test Todo', completed=True),
                                               Todo(title='Test Todo 1', completed=True),
                                               Todo(title='Test Todo 2', completed=False), ])

    def test_removed_all_completed_todo_ok(self):
        # Arrange
        remaining_expected_todos = 1

        # Act
        response = self.view.post(self.request)

        # Assert
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(['todo/partials/todo-app.html'], response.template_name)
        self.assertIn('checked', response.context_data)
        self.assertIn('todos', response.context_data)
        self.assertEqual(remaining_expected_todos, len(response.context_data.get('todos')))


