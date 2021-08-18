from django.db import models
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now


class PassedTasksDueDate(models.Manager):

    def get_passed_tasks(self):
        # data = super().get_queryset().annotate(Q(due_date__lt=Now()))
        data = super().get_queryset().filter(due_date__lt=Now())
        return data


class FullEmptyCategory(models.Manager):
    def get_empty_category(self):
        return [category for category in self.all() if not category.task_set.all()]

    def get_full_category(self):
        return [category for category in self.all() if category.task_set.all()]
