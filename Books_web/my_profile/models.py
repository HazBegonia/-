from django.db import models

from users.models import user_info

# Create your models here.
class SearchHistory(models.Model):
    user = models.ForeignKey(user_info, on_delete = models.CASCADE, related_name = 'search_histories')
    username = models.CharField(max_length = 20, null = True, blank = True)
    browse_books = models.CharField(max_length = 255)
    search_time = models.DateTimeField(auto_now_add = True)
    class Meta:
        db_table = 'search_history'
        ordering = ['-search_time']