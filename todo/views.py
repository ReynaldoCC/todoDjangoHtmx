from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import ProcessFormView

from todo.models import Todo


# Create your views here.
class HtmxResponseMixin(TemplateResponseMixin):
    htmx_template_name = None

    def get_template_names(self):
        if self.request.htmx and self.htmx_template_name:
            return [self.htmx_template_name]
        return super().get_template_names()


class TodoListView(HtmxResponseMixin, ListView):
    htmx_template_name = 'todo/partials/todo-app.html'
    template_name = 'todo/index.html'
    model = Todo
    context_object_name = 'todos'

    def get_context_data(self, *, object_list=None, **kwargs):
        filtered = self.request.GET.get('filters')
        filtered_by = filtered if filtered else ''
        self.extra_context = {
            'filter': filtered_by,
            'checked': Todo.objects.filter(completed=True).count()
        }
        return super().get_context_data(object_list=None, **kwargs)

    def get_queryset(self):
        if 'filters' in self.request.GET:
            filter_string = self.request.GET.get('filters')
            filter_qs = {filter_string.split('=')[0]: filter_string.split('=')[-1]} if '=' in filter_string else {}
            qs = super().get_queryset()
            return qs.filter(**filter_qs)
        return super().get_queryset()


class CreationTodoView(HtmxResponseMixin, CreateView):
    htmx_template_name = 'todo/partials/todo-app.html'
    model = Todo
    fields = ['title']

    def form_valid(self, form):
        form.save()
        context = {
            'todos': Todo.objects.all(),
        }
        return self.render_to_response(context)


class DeleteTodoView(HtmxResponseMixin, DeleteView):
    htmx_template_name = 'todo/partials/todo-app.html'
    model = Todo
    context_object_name = 'todo'

    def delete(self, request, *args, **kwargs):
        todo = self.get_object()
        todo.delete()
        context = {
            'todos': Todo.objects.all(),
            'checked': Todo.objects.filter(completed=True).count()
        }
        return self.render_to_response(context)


class UpdateTodoView(HtmxResponseMixin, UpdateView):
    htmx_template_name = 'todo/partials/todo-item.html'
    model = Todo
    context_object_name = 'todo'
    fields = ['title']

    def form_valid(self, form):
        todo = form.save()
        return self.render_to_response({'todo': todo})


class ToggleCompleteView(HtmxResponseMixin, UpdateView):
    htmx_template_name = 'todo/partials/todo-app.html'
    model = Todo
    fields = ['completed']

    def put(self, request, *args, **kwargs):
        todo = self.get_object()
        todo.completed = not todo.completed
        todo.save()
        context = {'todos': Todo.objects.all(),
                   'checked': Todo.objects.filter(completed=True).count()}
        return self.render_to_response(context=context)
