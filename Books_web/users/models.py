from django.db import models

# Create your models here.

class user_info(models.Model):
    user_name = models.CharField(max_length = 20, unique = True)
    password = models.CharField(max_length = 255)
    create_time = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'user_info'