from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

class MainNewsBig(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='MainNewsBig/')
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class MainNews(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='MainNews/')
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.title

class TrendingNews(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='TrendingNews/')
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='TrendingNews/')
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class VideoNews(models.Model):
    title = models.CharField(max_length=200)
    video = models.URLField(max_length=800)
    image = models.ImageField(upload_to='VideoNews/')
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class ListNews(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ListNews/')
    date = models.DateTimeField(auto_now_add=True)
    publisher = models.CharField(max_length=200)
    content = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

class TrendingNewsList(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='TrendingNewsList/')
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title