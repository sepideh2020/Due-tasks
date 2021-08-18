from multiprocessing.managers import Server

from django import forms
from django.template.defaultfilters import slugify

from apps.todo.models import Category, Task
from django.utils.timezone import now
from django.core.exceptions import ValidationError


class RegisterCategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name',]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if name == '':
            raise ValidationError('Please insert a Name')



class RegisterTaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'due_date', 'priority', 'done',]
        ordering = ['due_date',]

