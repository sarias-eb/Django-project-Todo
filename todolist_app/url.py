from django.urls import path
from .views import TodoListView, TodoListCreateView, TodoListUpdateView, TodoListDeleteView, TodoListReAssignView,TodoShowCreatedView
from django.urls import path, include


urlpatterns = [
	path('accounts/', include('django.contrib.auth.urls')),
    path('', TodoListView.as_view(), name='todo_list'),
    path('create/', TodoListCreateView.as_view(), name='todo_create'),
    path('update/<pk>', TodoListUpdateView.as_view(), name='todo_update'),
    path('delete/<pk>', TodoListDeleteView.as_view(), name='todo_delete'),
    path('reasign/<pk>', TodoListReAssignView.as_view(), name='todo_reassign'),
    path('view/<pk>', TodoShowCreatedView.as_view(), name='todo_view'),
]

