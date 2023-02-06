from django.db import models


class Category(models.Model):
    name = models.CharField('カテゴリー名', max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField('書籍名', max_length=300, blank=False, )
    fk_category = models.ForeignKey(to=Category, verbose_name='カテゴリー', on_delete=models.CASCADE, )
    price = models.PositiveIntegerField('価格', blank=False, )
    description = models.TextField('説明', max_length=500, )

    def __str__(self):
        return self.title
