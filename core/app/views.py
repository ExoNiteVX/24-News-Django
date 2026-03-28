from django.shortcuts import render

from .models import MainNewsBig, MainNews, TrendingNews, News, VideoNews, ListNews, TrendingNewsList, Category


# Create your views here.


def index(request):
    main= MainNewsBig.objects.all()
    mini_main =  MainNews.objects.all()
    trending = TrendingNews.objects.all()
    news = News.objects.all()
    video = VideoNews.objects.all()
    listnews = ListNews.objects.all()
    trendingnews = TrendingNewsList.objects.all()
    category = Category.objects.all()

    ctx = {
        'main':main,
        'mini_main':mini_main,
        'trending':trending,
        'news':news,
        'video':video,
        'listnews':listnews,
        'trendingnews':trendingnews,
        'category':category,
    }

    return render(request, 'index.html', ctx)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'Contact_us.html')

def technology(request):
    return render(request, 'technology.html')

def blog(request):
    return render(request, 'blog.html')

def events(request):
    return render(request, 'events.html')

def forums(request):
    return render(request, 'forums.html')

def single(request):
    return render(request, 'single.html')

def groups(request):
    return render(request, 'groups.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def science(request):
    return render(request, 'science.html')

def politics(request):
    return render(request, 'politics.html')

def business(request):
    return render(request, 'business.html')

def members(request):
    return render(request, 'members.html')

