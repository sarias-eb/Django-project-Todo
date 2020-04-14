from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic.detail import DetailView
# Create your views here.
from .models import ToDo
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


class TodoListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ToDo.objects.filter(asigned_user=self.request.user)
        return ToDo.objects


class TodoShowCreatedView(LoginRequiredMixin, DetailView):
    model = ToDo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def get_object(self):
        user = self.request.user
        item = super().get_object()
        if user.id != item.asigned_user.id:
            raise PermissionDenied
        else:
            return item


class TodoListCreateView(LoginRequiredMixin, CreateView):
    model = ToDo
    fields = ['title', 'description', 'asigned_user', 'done', 'created_by', 'updated_by', 'priority']

    def form_valid(self, form):  # debo sobreescribir para guardar datos
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('todo_view', args=(self.object.id,))


class TodoListUpdateView(LoginRequiredMixin, UpdateView):
    model = ToDo
    fields = ['title', 'description', 'asigned_user', 'done', 'created_by', 'updated_by', 'priority']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('todo_list')

    def get_object(self):
        user = self.request.user
        item = super().get_object()
        if user.id != item.asigned_user.id:
            raise PermissionDenied
        else:
            return item


class TodoListReAssignView(LoginRequiredMixin, UpdateView):
    model = ToDo
    fields = ['asigned_user', 'priority']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('todo_list')


class TodoListDeleteView(LoginRequiredMixin, DeleteView):
    model = ToDo
    success_url = reverse_lazy('todo_list')

    def get_success_url(self):
        return reverse('todo_view', args=(self.object.id,))
        return reverse('todo_view', args=(self.object.id,))

    def get_object(self):
        user = self.request.user
        item = super().get_object()
        if user.id != item.asigned_user.id:
            raise PermissionDenied
        else:
            return item
