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

class BookCollection(models.Model):
    user = models.ForeignKey(user_info, on_delete=models.CASCADE, db_column='username_id', verbose_name="用户")
    book_upc = models.CharField(max_length=50, verbose_name="书名编号")
    book_name = models.CharField(max_length=50, verbose_name="书名")
    collect_time = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间")
    class Meta:
        db_table = 'book_collection'
        ordering = ['-collect_time']

    def __str__(self):
        return f"{self.user.user_name} 收藏了 {self.book_name}"