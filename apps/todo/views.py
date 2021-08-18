from random import random
from django.shortcuts import render
from django.urls import reverse, NoReverseMatch

from apps.todo.models import Task, Category
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView
from django.core.serializers import serialize, deserialize
from apps.todo.forms import RegisterCategoryModelForm, RegisterTaskModelForm
from django.views.generic import ListView


class TaskList(ListView):
    model = Task
    context_object_name = 'task_list'


class TaskDetail(DetailView):
    model = Task
    template_name = 'todo/task_detail.html'


class IndexPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_Task'] = Task.objects.all()[:3]
        context['PassedTask'] = Task.objects.get_passed_tasks()
        context['EmptyCategory'] = Category.objects.get_full_category()
        context['full_category'] = Category.objects.get_full_category()
        context['empty_category'] = Category.objects.get_empty_category()

        return context


class CategoryList(ListView):
    model = Category
    context_object_name = 'categories_list'


class ListTaskCategory(DetailView):
    model = Category
    context_object_name = 'list_task_category'
    template_name = 'todo/ListTaskCategory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryView(View):
    def get(self, request):
        form = RegisterCategoryModelForm(request.Post)
        return render(request, 'todo/register_category.html', {'form': form})

    def post(self, request):
        form = RegisterTaskModelForm(request.Post)
        if form.is_valid():
            validated_data = form.cleaned_data
            category_obj = Category(**validated_data)
            category_obj.save()
            return redirect('saved Successfully')
        return render(request, 'todo/register_category.html', {'form': form})


class AddNewTask(View):  # a form for add task
    def get(self, request):
        form = RegisterTaskModelForm()
        return render(request, 'todo/register_task.html', {'form': form})

    def post(self, request):
        form = RegisterTaskModelForm(request.POST)
        if form.is_valid():
            validated_data = form.cleaned_data
            task_obj = Task(**validated_data)
            task_obj.save()
            return redirect('ok')

        return render(request, 'todo/register_task.html', {'form': form})


class AddNewCategory(View):  # a form for add category
    def get(self, request):
        form = RegisterCategoryModelForm()
        return render(request, 'todo/register_category.html', {'form': form})

    def post(self, request):
        form = RegisterCategoryModelForm(request.POST)
        if form.is_valid():
            validated_data = form.cleaned_data
            category_obj = Category(**validated_data)
            category_obj.save()
            return redirect('ok')  # go to the address' successfully'
        return render(request, 'todo/register_category.html', {'form': form})
