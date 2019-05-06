from django.urls import path

from task.views import TodoListView, TodoCreateView, TodoDeleteView, TodoUpdateView, TodoExportView, TodoImportView, \
    UserStatisticsView, UserProfileView

app_name = 'task'

urlpatterns = [
    path('todo_list/', TodoListView.as_view(), name='todo_list'),
    path('todo_create/', TodoCreateView.as_view(), name='todo_create'),
    path('todo_delete/<int:id>/', TodoDeleteView.as_view(), name='todo_delete'),

    path('todo_update/complete/<int:id>/', TodoUpdateView.as_view(), name='todo_update_complete'),
    path('todo_update/uncomplete/<int:id>/', TodoUpdateView.as_view(), name='todo_update_uncomplete'),

    path('todo_export/', TodoExportView.as_view(), name='todo_export'),
    path('todo_import/', TodoImportView.as_view(), name='todo_import'),

    path('user_statistics/', UserStatisticsView.as_view(), name='user_statistics'),
    path('user_profile/', UserProfileView.as_view(), name='user_profile'),
]