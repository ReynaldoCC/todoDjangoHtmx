from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Todo(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=255, default='')
    completed = models.BooleanField(verbose_name=_('Completed'), default=False, blank=True)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title
