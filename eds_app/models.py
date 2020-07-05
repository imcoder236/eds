from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class users_type_permission(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_type = models.PositiveSmallIntegerField(default=0)
    DateTime = models.DateTimeField(null=True)

class user_report(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    in_time = models.DateTimeField(null=True)
    out_time = models.DateTimeField(null=True)
