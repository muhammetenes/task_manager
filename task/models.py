from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


class Todo(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    text = models.TextField(_(u'To do text'))
    is_completed = models.BooleanField(_(u'Task status'), default=False)
    created_time = models.DateTimeField(_(u'Time when task created'), auto_now_add=True)
    last_updated = models.DateTimeField(_(u'Last time when task updated'), auto_now=True)

    class Meta:
        ordering = ('-id',)

    @property
    def get_user_full_name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)
