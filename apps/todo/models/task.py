from datetime import date

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import NoReverseMatch, reverse
from django.utils.timezone import now

from apps.todo.manager import PassedTasksDueDate, FullEmptyCategory


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name', unique=True)
    slug = models.SlugField(max_length=100, verbose_name='Slug')
    objects = FullEmptyCategory()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # for auto slugging the forms slug
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Task(models.Model):
    title = models.CharField('Title', max_length=250, unique=True)  # a varchar
    slug = models.SlugField(verbose_name='Slug')
    description = models.TextField('Description', blank=True)  # a text field
    PRIORITY_CHOICES = (
        ('V-Imp', '!!!'),
        ('Imp', '!!'),
        ('N-V-Imp', '!'),
        ('N-Imp', 'None'),
    )
    priority = models.CharField(verbose_name='Priority', max_length=7, choices=PRIORITY_CHOICES)
    due_date = models.DateTimeField(default=now)  # a date
    created = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(verbose_name='Done', default=False)
    category = models.ForeignKey('Category', default="general", on_delete=models.PROTECT)  # a foreignkey
    objects = PassedTasksDueDate()

    class Meta:
        ordering = ["due_date"]

    def __str__(self):
        return self.title

    @property
    def calculate_due_date(self):
        if self.due_date:
            today = date.today()
            return "{},{},{}".format(today.year - self.due_date.year, today.month - self.due_date.month,
                                     today.day - self.due_date.day)

    def get_absolute_url(self):
        try:
            return reverse('tasks_detail', args=(str(self.id)))
        except NoReverseMatch:
            return reverse('404')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
