from django.db import models

# Create your models here.

class Book(models.Model):
    book_name = models.CharField(max_length = 255)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    subject = models.CharField(max_length = 255)
    stock = models.IntegerField(default = 0)
    reviewers = models.IntegerField(default = 0)
    UPC = models.CharField(max_length = 50, unique = True)
    description = models.TextField()
    rating = models.IntegerField(default = 0)
    image = models.URLField(max_length = 500)

    class Meta:
        db_table = 'book_info'