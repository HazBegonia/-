# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BookInfo(models.Model):
    name = models.CharField(max_length=255, db_comment='书名')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_comment='价格')
    subject = models.CharField(max_length=255, db_comment='类型')
    stock = models.IntegerField(blank=True, null=True, db_comment='库存数量')
    reviewers = models.IntegerField(blank=True, null=True, db_comment='评论数量')
    upc = models.CharField(db_column='UPC', max_length=50, db_comment='唯一标识码')  # Field name made lowercase.
    description = models.TextField(blank=True, null=True, db_comment='书籍简介')
    rating = models.IntegerField(blank=True, null=True, db_comment='评分')
    image = models.CharField(max_length=500, blank=True, null=True, db_comment='图片URL地址')
    created_at = models.DateTimeField(blank=True, null=True, db_comment='抓取时间')

    class Meta:
        managed = False
        db_table = 'book_info'
