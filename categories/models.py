from django.db import models


class Category(models.Model):
    cat_name = models.CharField(max_length=50)

    def __str__(self):
        return self.cat_name


class Genre(models.Model):
    gen_name = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.gen_name
