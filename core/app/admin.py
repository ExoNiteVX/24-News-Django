from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    MainNewsBig, MainNews, TrendingNews, News,
    VideoNews, ListNews, TrendingNewsList, Category
)

models = [
    MainNewsBig, MainNews, TrendingNews, News,
    VideoNews, ListNews, TrendingNewsList, Category
]

for model in models:
    @admin.register(model)
    class CustomAdmin(ModelAdmin):
        pass