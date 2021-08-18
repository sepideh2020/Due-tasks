from django.urls import include, path
from django.views.generic import TemplateView

from apps.todo.models import Task
from apps.todo.views import TaskList, TaskDetail, CategoryList, AddNewTask, AddNewCategory, ListTaskCategory

urlpatterns = [
    path('tasks/', include([
        path('', TaskList.as_view(), name='tasks'),
        # path('<slug:slug>/', TaskDetail.as_view(), name='tasks_detail'),
        path('<int:pk>/', TaskDetail.as_view(), name='tasks_detail'),
    ])),
    path('AddNewTask/', AddNewTask.as_view(), name='add_new_task'),
    path('AddNewCategory/', AddNewCategory.as_view(), name='add_new_category'),

    path('categories/', include([
        path('', CategoryList.as_view(), name='categories'),
        path('<slug:slug>/', ListTaskCategory.as_view(), name='ListTaskCategory'),
    ])),


]
