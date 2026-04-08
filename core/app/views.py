from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

from .models import MainNewsBig, MainNews, TrendingNews, News, VideoNews, ListNews, TrendingNewsList, Category, \
    SinglePage, About, LastlyModified, Forum, Group, Member, Event, UserProfile, VerificationCode, NewsletterSubscriber, \
    Tag, Comment, Bookmark, LikeDislike, CommentVote, SocialMedia, TelegramSetting, TelegramLog
from .utils import generate_code


def index(request):
    all_posts = []
    
    for item in MainNewsBig.objects.all():
        all_posts.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'model_type': 'main_big',
            'id': item.id,
        })
    
    for item in MainNews.objects.all():
        all_posts.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'model_type': 'main',
            'id': item.id,
        })
    
    for item in TrendingNews.objects.all():
        all_posts.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'publisher': item.publisher,
            'model_type': 'trending',
            'id': item.id,
        })
    
    for item in News.objects.all():
        all_posts.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'model_type': 'news',
            'id': item.id,
        })
    
    for item in VideoNews.objects.all():
        all_posts.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'video': item.video,
            'model_type': 'video',
            'id': item.id,
        })
    
    for item in ListNews.objects.all():
        all_posts.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'publisher': item.publisher,
            'content': item.content,
            'model_type': 'list',
            'id': item.id,
        })
    
    for item in TrendingNewsList.objects.all():
        all_posts.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'model_type': 'trending_list',
            'id': item.id,
        })
    
    all_posts.sort(key=lambda x: x['date'], reverse=True)
    
    main = all_posts[:1]
    mini_main = all_posts[1:5]
    trending = all_posts[:5]
    news = all_posts[:4]
    
    video = VideoNews.objects.all()
    listnews = ListNews.objects.all()
    trendingnews = TrendingNewsList.objects.all()
    category = Category.objects.all()
    about = About.objects.all()
    modified_lastly = LastlyModified.objects.all()
    
    main_page = SinglePage.objects.filter(is_main_page=True).first() or SinglePage.objects.first()
    about_page = SinglePage.objects.filter(is_about_page=True).first() or SinglePage.objects.first()
    breaking_news = MainNewsBig.objects.filter(is_breaking=True).first() or MainNewsBig.objects.first()
    
    lastly_modified_pages = SinglePage.objects.all().order_by('-updated_at')[:5]

    search = request.GET.get('search', '').strip()
    category_slug = request.GET.get('category', '')

    if search:
        listnews = listnews.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search)
        )

    if category_slug:
        listnews = listnews.filter(category__slug=category_slug)

    other_new = list(listnews[:5])

    paginator = Paginator(listnews, 10)
    page_number = request.GET.get('page')
    listnews_paginated = paginator.get_page(page_number)

    all_posts_sorted = sorted(all_posts, key=lambda x: getattr(x, 'views', 0) or 0, reverse=True)
    most_viewed = all_posts_sorted[:3]

    ctx = {
        'main': main,
        'mini_main': mini_main,
        'trending': trending,
        'news': news,
        'video': video,
        'listnews': listnews,
        'trendingnews': trendingnews,
        'category': category,
        'about': main_page,
        'about_page': about_page,
        'about_description': about,
        'lastly': modified_lastly,
        'breaking_news': breaking_news,
        'main_page': main_page,
        'all_posts': all_posts,
        'most_viewed': most_viewed,
        'categories': category,
        'listnews_paginated': listnews_paginated,
        'other_new': other_new,
        'search': search,
        'category_slug': category_slug,
        'lastly_modified_pages': lastly_modified_pages,
    }

    return render(request, 'index.html', ctx)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        if name and email and subject and message:
            full_message = f"From: {name} <{email}>\n\n{message}"
            try:
                send_mail(
                    subject=f"Contact Form: {subject}",
                    message=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL or email,
                    recipient_list=[settings.EMAIL_HOST_USER or 'admin@example.com'],
                    fail_silently=True,
                )
                messages.success(request, 'Your message has been sent successfully!')
            except Exception:
                messages.error(request, 'There was an error sending your message. Please try again later.')
        else:
            messages.error(request, 'Please fill in all fields.')
        
        return redirect('contact')
    
    social_media = SocialMedia.objects.filter(is_active=True)
    category = Category.objects.all()
    trendingnews = TrendingNewsList.objects.all()
    about = SinglePage.objects.filter(is_about_page=True).first()
    
    return render(request, 'Contact_us.html', {
        'social_media': social_media,
        'category': category,
        'trendingnews': trendingnews,
        'about': about,
    })

def get_category_news(category):
    if not category:
        return []
    
    all_posts = []
    
    for item in MainNewsBig.objects.filter(category=category):
        all_posts.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'model_type': 'main_big',
            'id': item.id,
        })
    
    for item in MainNews.objects.filter(category=category):
        all_posts.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'model_type': 'main',
            'id': item.id,
        })
    
    for item in TrendingNews.objects.filter(category=category):
        all_posts.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'publisher': item.publisher,
            'model_type': 'trending',
            'id': item.id,
        })
    
    for item in News.objects.filter(category=category):
        all_posts.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'model_type': 'news',
            'id': item.id,
        })
    
    for item in VideoNews.objects.filter(category=category):
        all_posts.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'video': item.video,
            'model_type': 'video',
            'id': item.id,
        })
    
    for item in ListNews.objects.filter(category=category):
        all_posts.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'publisher': item.publisher,
            'content': item.content,
            'model_type': 'list',
            'id': item.id,
        })
    
    for item in TrendingNewsList.objects.filter(category=category):
        all_posts.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'model_type': 'trending_list',
            'id': item.id,
        })
    
    all_posts.sort(key=lambda x: x['date'], reverse=True)
    
    return all_posts


def technology(request):
    tech_category = Category.objects.filter(slug__iexact='technology').first() or \
                   Category.objects.filter(name__icontains='Technology').first()
    
    tech_news = get_category_news(tech_category) if tech_category else []
    
    search = request.GET.get('search', '').strip()
    if search:
        tech_news = [n for n in tech_news if search.lower() in n['title'].lower()]
    
    paginator = Paginator(tech_news, 6)
    page = request.GET.get('page')
    try:
        tech_news_paginated = paginator.page(page)
    except PageNotAnInteger:
        tech_news_paginated = paginator.page(1)
    except EmptyPage:
        tech_news_paginated = paginator.page(paginator.num_pages)
    
    about = SinglePage.objects.first()
    about_description = About.objects.all()
    category = Category.objects.all()
    trendingnews = TrendingNewsList.objects.all()
    lastly_modified_pages = SinglePage.objects.all().order_by('-updated_at')[:5]
    
    # Get top 5 posts for hero section
    hero_news = tech_news[:5] if tech_category else []
    
    return render(request, 'technology.html', {
        'page_news': tech_news_paginated,
        'page_title': 'Technology News',
        'about': about,
        'about_description': about_description,
        'category': category,
        'trendingnews': trendingnews,
        'search': search,
        'lastly_modified_pages': lastly_modified_pages,
        'hero_news': hero_news,
    })

def blog(request):
    all_news_list = News.objects.all().order_by('-date')
    
    search = request.GET.get('search', '').strip()
    if search:
        all_news_list = all_news_list.filter(
            Q(title__icontains=search)
        )
    
    paginator = Paginator(all_news_list, 10)
    page = request.GET.get('page')
    try:
        all_news = paginator.page(page)
    except PageNotAnInteger:
        all_news = paginator.page(1)
    except EmptyPage:
        all_news = paginator.page(paginator.num_pages)
    
    about = SinglePage.objects.first()
    about_description = About.objects.all()
    category = Category.objects.all()
    trendingnews = TrendingNewsList.objects.all()
    lastly_modified_pages = SinglePage.objects.all().order_by('-updated_at')[:5]
    return render(request, 'blog.html', {
        'all_news': all_news,
        'about': about,
        'about_description': about_description,
        'category': category,
        'trendingnews': trendingnews,
        'search': search,
        'lastly_modified_pages': lastly_modified_pages,
    })

def events(request):
    events_list = Event.objects.all().order_by('-date')
    about = SinglePage.objects.first()
    about_description = About.objects.all()
    category = Category.objects.all()
    trendingnews = TrendingNewsList.objects.all()
    lastly_modified_pages = SinglePage.objects.all().order_by('-updated_at')[:5]

    hero_events = events_list[:5]
    
    return render(request, 'events.html', {
        'events': events_list,
        'hero_events': hero_events,
        'about': about,
        'about_description': about_description,
        'category': category,
        'trendingnews': trendingnews,
        'lastly_modified_pages': lastly_modified_pages,
    })

def forums(request):
    forums = Forum.objects.all().order_by('-date')
    about = SinglePage.objects.first()
    about_description = About.objects.all()
    category = Category.objects.all()
    trendingnews = TrendingNewsList.objects.all()
    lastly_modified_pages = SinglePage.objects.all().order_by('-updated_at')[:5]
    return render(request, 'forums.html', {
        'forums': forums,
        'about': about,
        'about_description': about_description,
        'category': category,
        'trendingnews': trendingnews,
        'lastly_modified_pages': lastly_modified_pages,
    })

def groups(request):
    groups = Group.objects.all().order_by('-date')
    about = SinglePage.objects.first()
    about_description = About.objects.all()
    category = Category.objects.all()
    trendingnews = TrendingNewsList.objects.all()
    lastly_modified_pages = SinglePage.objects.all().order_by('-updated_at')[:5]
    return render(request, 'groups.html', {
        'groups': groups,
        'about': about,
        'about_description': about_description,
        'category': category,
        'trendingnews': trendingnews,
        'lastly_modified_pages': lastly_modified_pages,
    })

def business(request):
    business_category = Category.objects.filter(slug__iexact='business').first() or \
                       Category.objects.filter(name__icontains='Business').first()
    
    business_news = get_category_news(business_category) if business_category else []
    
    search = request.GET.get('search', '').strip()
    if search:
        business_news = [n for n in business_news if search.lower() in n['title'].lower()]
    
    paginator = Paginator(business_news, 6)
    page = request.GET.get('page')
    try:
        business_news_paginated = paginator.page(page)
    except PageNotAnInteger:
        business_news_paginated = paginator.page(1)
    except EmptyPage:
        business_news_paginated = paginator.page(paginator.num_pages)
    
    about = SinglePage.objects.first()
    about_description = About.objects.all()
    category = Category.objects.all()
    trendingnews = TrendingNewsList.objects.all()
    lastly_modified_pages = SinglePage.objects.all().order_by('-updated_at')[:5]

    hero_news = business_news[:5] if business_category else []
    
    return render(request, 'business.html', {
        'page_news': business_news_paginated,
        'page_title': 'Business News',
        'about': about,
        'about_description': about_description,
        'category': category,
        'trendingnews': trendingnews,
        'search': search,
        'lastly_modified_pages': lastly_modified_pages,
        'hero_news': hero_news,
    })

def science(request):
    science_category = Category.objects.filter(slug__iexact='science').first() or \
                      Category.objects.filter(name__icontains='Science').first()
    
    science_news = get_category_news(science_category) if science_category else []
    
    search = request.GET.get('search', '').strip()
    if search:
        science_news = [n for n in science_news if search.lower() in n['title'].lower()]
    
    paginator = Paginator(science_news, 6)
    page = request.GET.get('page')
    try:
        science_news_paginated = paginator.page(page)
    except PageNotAnInteger:
        science_news_paginated = paginator.page(1)
    except EmptyPage:
        science_news_paginated = paginator.page(paginator.num_pages)
    
    about = SinglePage.objects.first()
    about_description = About.objects.all()
    category = Category.objects.all()
    trendingnews = TrendingNewsList.objects.all()
    lastly_modified_pages = SinglePage.objects.all().order_by('-updated_at')[:5]

    hero_news = science_news[:5] if science_category else []
    
    return render(request, 'science.html', {
        'page_news': science_news_paginated,
        'page_title': 'Science News',
        'about': about,
        'about_description': about_description,
        'category': category,
        'trendingnews': trendingnews,
        'search': search,
        'lastly_modified_pages': lastly_modified_pages,
        'hero_news': hero_news,
    })

def politics(request):
    politics_category = Category.objects.filter(slug__iexact='politics').first() or \
                         Category.objects.filter(name__icontains='Politics').first()
    
    politics_news = get_category_news(politics_category) if politics_category else []
    
    search = request.GET.get('search', '').strip()
    if search:
        politics_news = [n for n in politics_news if search.lower() in n['title'].lower()]
    
    paginator = Paginator(politics_news, 6)
    page = request.GET.get('page')
    try:
        politics_news_paginated = paginator.page(page)
    except PageNotAnInteger:
        politics_news_paginated = paginator.page(1)
    except EmptyPage:
        politics_news_paginated = paginator.page(paginator.num_pages)
    
    about = SinglePage.objects.first()
    about_description = About.objects.all()
    category = Category.objects.all()
    trendingnews = TrendingNewsList.objects.all()
    lastly_modified_pages = SinglePage.objects.all().order_by('-updated_at')[:5]

    hero_news = politics_news[:5] if politics_category else []
    
    return render(request, 'politics.html', {
        'page_news': politics_news_paginated,
        'page_title': 'Politics News',
        'about': about,
        'about_description': about_description,
        'category': category,
        'trendingnews': trendingnews,
        'search': search,
        'lastly_modified_pages': lastly_modified_pages,
        'hero_news': hero_news,
    })

def members(request):
    members = Member.objects.filter(is_active=True).order_by('-date_joined')
    about = SinglePage.objects.first()
    about_description = About.objects.all()
    category = Category.objects.all()
    trendingnews = TrendingNewsList.objects.all()
    lastly_modified_pages = SinglePage.objects.all().order_by('-updated_at')[:5]
    return render(request, 'members.html', {
        'members': members,
        'about': about,
        'about_description': about_description,
        'category': category,
        'trendingnews': trendingnews,
        'lastly_modified_pages': lastly_modified_pages,
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)

    news_items = News.objects.filter(category=category)
    main_big_items = MainNewsBig.objects.filter(category=category)
    main_items = MainNews.objects.filter(category=category)
    trending_items = TrendingNews.objects.filter(category=category)
    video_items = VideoNews.objects.filter(category=category)
    list_items = ListNews.objects.filter(category=category)
    single_items = SinglePage.objects.filter(category=category)

    all_items = []
    
    for item in main_big_items:
        all_items.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'model_type': 'main_big',
            'id': item.id,
            'is_featured': item.is_featured,
            'is_breaking': item.is_breaking,
        })
    
    for item in main_items:
        all_items.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'model_type': 'main',
            'id': item.id,
            'is_featured': item.is_featured,
        })
    
    for item in news_items:
        all_items.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'model_type': 'news',
            'id': item.id,
            'is_featured': item.is_featured,
        })
    
    for item in trending_items:
        all_items.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'publisher': item.publisher,
            'model_type': 'trending',
            'id': item.id,
        })
    
    for item in video_items:
        all_items.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'video': item.video,
            'model_type': 'video',
            'id': item.id,
        })
    
    for item in list_items:
        all_items.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'publisher': item.publisher,
            'content': item.content,
            'model_type': 'list',
            'id': item.id,
            'is_featured': item.is_featured,
        })
    
    for item in single_items:
        all_items.append({
            'title': item.title,
            'image': item.image,
            'date': item.created_at,
            'views': item.views,
            'category': item.category,
            'model_type': 'single',
            'id': item.id,
            'is_featured': getattr(item, 'is_featured', False),
        })

    all_items.sort(key=lambda x: x['date'], reverse=True)

    page = request.GET.get('page', 1)
    paginator = Paginator(all_items, 12)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    
    about = SinglePage.objects.first()
    about_description = About.objects.all()
    category_list = Category.objects.all()
    trendingnews = TrendingNewsList.objects.all()
    
    return render(request, 'category_detail.html', {
        'category': category,
        'items': items,
        'page_title': f'{category.name} News',
        'meta_title': f"{category.name} News - 24 News",
        'meta_description': f"Latest {category.name} news, updates, and analysis from 24 News",
        'meta_keywords': f"{category.name}, news, latest news, {category.name} updates",
        'about': about,
        'about_description': about_description,
        'category_list': category_list,
        'trendingnews': trendingnews,
        'total_count': len(all_items),
    })

def single(request, id):
    about_page = get_object_or_404(SinglePage, id=id)
    
    SinglePage.objects.filter(id=id).update(views=F('views') + 1)
    about_page.refresh_from_db()

    comments = Comment.objects.filter(single_page=about_page, is_approved=True).select_related('author').order_by('-created_at')

    user_bookmarks = []
    if request.user.is_authenticated:
        user_bookmarks = Bookmark.objects.filter(
            user=request.user, 
            single_page=about_page
        ).values_list('single_page_id', flat=True)

    related_news = []
    if about_page.category:
        related_news = SinglePage.objects.filter(
            category=about_page.category
        ).exclude(id=id).order_by('-created_at')[:4]
    
    if not related_news and about_page.tags.exists():
        related_news = SinglePage.objects.filter(
            tags__in=about_page.tags.all()
        ).exclude(id=id).distinct().order_by('-created_at')[:4]
    
    about = SinglePage.objects.first()
    about_description = About.objects.all()
    category = Category.objects.all()
    trendingnews = TrendingNewsList.objects.all()

    author_profile = None
    if about_page.author:
        author_profile, _ = UserProfile.objects.get_or_create(user=about_page.author)
    prev_article = SinglePage.objects.filter(
        created_at__lt=about_page.created_at
    ).order_by('-created_at').first()
    
    next_article = SinglePage.objects.filter(
        created_at__gt=about_page.created_at
    ).order_by('created_at').first()
    
    return render(request, 'single.html', {
        'about_page': about_page,
        'page_news': News.objects.all().order_by('-date')[:6],
        'page_title': about_page.title,
        'about': about,
        'about_description': about_description,
        'category': category,
        'trendingnews': trendingnews,
        'comments': comments,
        'user_bookmarks': list(user_bookmarks),
        'related_news': related_news,
        'author_profile': author_profile,
        'prev_article': prev_article,
        'next_article': next_article,
    })

@ratelimit(key='ip', rate='5/m', method='POST')
def login(request):
    if getattr(request, 'limited', False):
        messages.error(request, 'Too many login attempts. Please try again later.')
        return redirect('login')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'login.html')


def search(request):
    query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', 'all')
    category_slug = request.GET.get('category', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    sort_by = request.GET.get('sort', 'date_desc')
    results = []
    
    if query:
        news_results = News.objects.filter(title__icontains=query)
        video_results = VideoNews.objects.filter(title__icontains=query)
        trending_results = TrendingNews.objects.filter(title__icontains=query)
        list_results = ListNews.objects.filter(title__icontains=query)
        single_results = SinglePage.objects.filter(title__icontains=query)

        if filter_type == 'news':
            video_results = []
            trending_results = []
            list_results = []
            single_results = []
        elif filter_type == 'video':
            news_results = []
            trending_results = []
            list_results = []
            single_results = []
        elif filter_type == 'trending':
            news_results = []
            video_results = []
            list_results = []
            single_results = []
        elif filter_type == 'list':
            news_results = []
            video_results = []
            trending_results = []
            single_results = []
        elif filter_type == 'single':
            news_results = []
            video_results = []
            trending_results = []
            list_results = []

        if category_slug:
            news_results = news_results.filter(category__slug=category_slug) if news_results else []
            video_results = video_results.filter(category__slug=category_slug) if video_results else []
            trending_results = trending_results.filter(category__slug=category_slug) if trending_results else []
            list_results = list_results.filter(category__slug=category_slug) if list_results else []
            single_results = single_results.filter(category__slug=category_slug) if single_results else []

        if date_from:
            from_date = parse_date(date_from)
            if from_date:
                news_results = news_results.filter(date__gte=from_date) if news_results else []
                video_results = video_results.filter(date__gte=from_date) if video_results else []
                trending_results = trending_results.filter(date__gte=from_date) if trending_results else []
                list_results = list_results.filter(date__gte=from_date) if list_results else []
                single_results = single_results.filter(created_at__gte=from_date) if single_results else []
        
        if date_to:
            to_date = parse_date(date_to)
            if to_date:
                news_results = news_results.filter(date__lte=to_date) if news_results else []
                video_results = video_results.filter(date__lte=to_date) if video_results else []
                trending_results = trending_results.filter(date__lte=to_date) if trending_results else []
                list_results = list_results.filter(date__lte=to_date) if list_results else []
                single_results = single_results.filter(created_at__lte=to_date) if single_results else []

        for item in news_results:
            results.append({
                'title': item.title,
                'image': item.image,
                'date': item.date,
                'views': item.views,
                'category': item.category,
                'model_type': 'news',
                'id': item.id,
                'content': getattr(item, 'content', ''),
            })
        for item in video_results:
            results.append({
                'title': item.title,
                'image': item.image,
                'date': item.date,
                'views': item.views,
                'category': item.category,
                'video': item.video,
                'model_type': 'video',
                'id': item.id,
            })
        for item in trending_results:
            results.append({
                'title': item.title,
                'image': item.image,
                'date': item.date,
                'views': item.views,
                'category': item.category,
                'publisher': item.publisher,
                'model_type': 'trending',
                'id': item.id,
            })
        for item in list_results:
            results.append({
                'title': item.title,
                'image': item.image,
                'date': item.date,
                'views': item.views,
                'category': item.category,
                'publisher': item.publisher,
                'content': item.content,
                'model_type': 'list',
                'id': item.id,
            })
        for item in single_results:
            results.append({
                'title': item.title,
                'image': item.image,
                'date': item.created_at,
                'views': item.views,
                'category': item.category,
                'model_type': 'single',
                'id': item.id,
            })

        if sort_by == 'date_asc':
            results.sort(key=lambda x: x['date'])
        elif sort_by == 'views_desc':
            results.sort(key=lambda x: x['views'], reverse=True)
        elif sort_by == 'views_asc':
            results.sort(key=lambda x: x['views'])
        else:
            results.sort(key=lambda x: x['date'], reverse=True)

    page = request.GET.get('page', 1)
    paginator = Paginator(results, 10)
    try:
        results_paginated = paginator.page(page)
    except PageNotAnInteger:
        results_paginated = paginator.page(1)
    except EmptyPage:
        results_paginated = paginator.page(paginator.num_pages)
    
    about = SinglePage.objects.first()
    trendingnews = TrendingNewsList.objects.all()
    category = Category.objects.all()
    
    return render(request, 'search.html', {
        'results': results_paginated,
        'query': query,
        'filter_type': filter_type,
        'category_slug': category_slug,
        'date_from': date_from,
        'date_to': date_to,
        'sort_by': sort_by,
        'trendingnews': trendingnews,
        'category': category,
        'about': about,
        'total_results': len(results),
        'meta_title': f"Search Results for '{query}' - 24 News",
        'meta_description': f"Search results for {query}. Find the latest news and articles on 24 News.",
        'meta_keywords': f"search, {query}, news, articles",
    })

@ratelimit(key='ip', rate='10/m', method='POST')
def register(request):
    if getattr(request, 'limited', False):
        messages.error(request, 'Too many registration attempts. Please try again later.')
        return redirect('register')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')

        User.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1)
        messages.success(request, 'Registration Successful')
        return redirect('login')

    return render(request, 'register.html')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        bio = request.POST.get('bio')
        phone = request.POST.get('phone')
        remove_photo = request.POST.get('remove_photo') == 'true'
        
        if username:
            user.username = username
        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
            
        user.save()

        if bio is not None:
            user_profile.bio = bio
        if phone is not None:
            user_profile.phone = phone

        if remove_photo and user_profile.photo:
            user_profile.photo.delete(save=False)
            user_profile.photo = None

        if request.FILES.get('photo'):
            if user_profile.photo and not remove_photo:
                user_profile.photo.delete(save=False)
            user_profile.photo = request.FILES.get('photo')
            
        user_profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    user_comments = Comment.objects.filter(author=request.user).order_by('-created_at')[:10]

    bookmarks_count = Bookmark.objects.filter(user=request.user).count()

    articles_count = SinglePage.objects.filter(author=request.user).count()
    
    return render(request, 'profile.html', {
        'profile': user_profile,
        'user_comments': user_comments,
        'bookmarks_count': bookmarks_count,
        'articles_count': articles_count,
    })


def subscribe_view(request):
    return redirect('newsletter_subscribe')

def verify_email(request):
    if request.method == 'POST':
        user_code = request.POST.get('code', '').strip()

        verification = VerificationCode.objects.filter(code=user_code, is_used=False).first()

        if not verification:
            messages.error(request, 'Invalid verification code.')
            return redirect('verify_email_page')

        expiry_limit = verification.created_at + timedelta(minutes=15)
        if timezone.now() > expiry_limit:
            messages.error(request, 'This code has expired. Please request a new one.')
            return redirect('newsletter_subscribe')

        verification.is_used = True
        verification.save()

        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=verification.email,
            defaults={'is_active': True}
        )
        if not created:
            subscriber.is_active = True
            subscriber.save()

        messages.success(request, 'Your email has been verified successfully!')
        return redirect('success_page')

    return render(request, 'verify_template.html')


def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            messages.error(request, 'Email cannot be empty!')
            return redirect('home')

        if NewsletterSubscriber.objects.filter(email=email, is_active=True).exists():
            messages.info(request, 'This email is already subscribed!')
            return redirect('home')

        code = generate_code()
        VerificationCode.objects.create(email=email, code=code)

        try:
            send_mail(
                subject='Verify your email',
                message=f'Verify your email by using {code}',
                from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=True,
            )
            messages.success(request, 'Verification code sent to your email!')
        except Exception as e:
            messages.warning(request, f'Email could not be sent: {str(e)}')

        return redirect('verify_email_page')

    return render(request, 'subscribe.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('home')


def about(request):
    trendingnews = TrendingNewsList.objects.all()
    category = Category.objects.all()
    about = SinglePage.objects.first()
    
    ctx = {
        'trendingnews': trendingnews,
        'category': category,
        'about': about,
    }
    
    return render(request, 'about.html', ctx)


def author_detail(request, user_id):
    author = get_object_or_404(User, id=user_id)
    author_profile, created = UserProfile.objects.get_or_create(user=author)

    articles_list = []

    for item in SinglePage.objects.filter(author=author).order_by('-created_at'):
        articles_list.append({
            'title': item.title,
            'image': item.image,
            'date': item.created_at,
            'views': item.views,
            'model_type': 'single',
            'id': item.id,
        })

    for model in [News, VideoNews, ListNews, TrendingNews]:
        if hasattr(model, 'author'):
            for item in model.objects.filter(author=author).order_by('-date' if hasattr(model, 'date') else '-created_at'):
                articles_list.append({
                    'title': item.title,
                    'image': item.image,
                    'date': item.date if hasattr(item, 'date') else item.created_at,
                    'views': item.views,
                    'model_type': model.__name__.lower(),
                    'id': item.id,
                })

    articles_list.sort(key=lambda x: x['date'], reverse=True)

    page = request.GET.get('page', 1)
    paginator = Paginator(articles_list, 9)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    total_views = sum(a['views'] for a in articles_list)
    
    ctx = {
        'author': author,
        'author_profile': author_profile,
        'articles': articles,
        'articles_count': len(articles_list),
        'total_views': total_views,
    }
    
    return render(request, 'author_detail.html', ctx)


def success_view(request):
    return render(request, 'success.html')


@login_required
@ratelimit(key='ip', rate='3/m', method='POST')
def add_comment(request):
    if getattr(request, 'limited', False):
        messages.error(request, 'Please wait before posting another comment.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        single_page_id = request.POST.get('single_page_id')
        news_id = request.POST.get('news_id')
        list_news_id = request.POST.get('list_news_id')
        trending_news_id = request.POST.get('trending_news_id')
        parent_id = request.POST.get('parent_id')
        
        if not content:
            messages.error(request, 'Comment cannot be empty!')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        
        comment_data = {
            'author': request.user,
            'content': content,
        }
        
        if single_page_id:
            comment_data['single_page_id'] = single_page_id
        elif news_id:
            comment_data['news_id'] = news_id
        elif list_news_id:
            comment_data['list_news_id'] = list_news_id
        elif trending_news_id:
            comment_data['trending_news_id'] = trending_news_id
            
        if parent_id:
            comment_data['parent_id'] = parent_id
            
        Comment.objects.create(**comment_data)
        messages.success(request, 'Comment added successfully!')
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
    return redirect('home')


@login_required
def toggle_bookmark(request):
    if request.method == 'POST':
        single_page_id = request.POST.get('single_page_id')
        news_id = request.POST.get('news_id')
        list_news_id = request.POST.get('list_news_id')
        trending_news_id = request.POST.get('trending_news_id')
        
        bookmark_data = {'user': request.user}
        
        if single_page_id:
            bookmark_data['single_page_id'] = single_page_id
            existing = Bookmark.objects.filter(user=request.user, single_page_id=single_page_id).first()
        elif news_id:
            bookmark_data['news_id'] = news_id
            existing = Bookmark.objects.filter(user=request.user, news_id=news_id).first()
        elif list_news_id:
            bookmark_data['list_news_id'] = list_news_id
            existing = Bookmark.objects.filter(user=request.user, list_news_id=list_news_id).first()
        elif trending_news_id:
            bookmark_data['trending_news_id'] = trending_news_id
            existing = Bookmark.objects.filter(user=request.user, trending_news_id=trending_news_id).first()
        else:
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        
        if existing:
            existing.delete()
            messages.success(request, 'Bookmark removed!')
        else:
            Bookmark.objects.create(**bookmark_data)
            messages.success(request, 'Bookmark added!')
            
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
    return redirect('home')


@login_required
def vote(request):
    if request.method == 'POST':
        vote_type = request.POST.get('vote_type')
        single_page_id = request.POST.get('single_page_id')
        news_id = request.POST.get('news_id')
        list_news_id = request.POST.get('list_news_id')
        
        vote_value = LikeDislike.LIKE if vote_type == 'like' else LikeDislike.DISLIKE
        vote_data = {'user': request.user, 'vote': vote_value}
        
        if single_page_id:
            vote_data['single_page_id'] = single_page_id
            existing = LikeDislike.objects.filter(user=request.user, single_page_id=single_page_id).first()
            page = SinglePage.objects.get(id=single_page_id)
        elif news_id:
            vote_data['news_id'] = news_id
            existing = LikeDislike.objects.filter(user=request.user, news_id=news_id).first()
            page = None
        elif list_news_id:
            vote_data['list_news_id'] = list_news_id
            existing = LikeDislike.objects.filter(user=request.user, list_news_id=list_news_id).first()
            page = None
        else:
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        
        if existing:
            if existing.vote == vote_value:
                existing.delete()
                if page:
                    if vote_type == 'like':
                        page.likes = max(0, page.likes - 1)
                    else:
                        page.dislikes = max(0, page.dislikes - 1)
                    page.save()
                messages.success(request, f'{vote_type.capitalize()} removed!')
            else:
                if page:
                    if vote_type == 'like':
                        page.likes += 1
                        page.dislikes = max(0, page.dislikes - 1)
                    else:
                        page.dislikes += 1
                        page.likes = max(0, page.likes - 1)
                    page.save()
                existing.vote = vote_value
                existing.save()
                messages.success(request, f'Vote changed to {vote_type}!')
        else:
            LikeDislike.objects.create(**vote_data)
            if page:
                if vote_type == 'like':
                    page.likes += 1
                else:
                    page.dislikes += 1
                page.save()
            messages.success(request, f'{vote_type.capitalize()} added!')
            
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
    return redirect('home')


@login_required
def my_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related(
        'single_page', 'news', 'list_news', 'trending_news'
    ).order_by('-created_at')
    
    trendingnews = TrendingNewsList.objects.all()
    category = Category.objects.all()
    about = SinglePage.objects.first()
    
    ctx = {
        'bookmarks': bookmarks,
        'trendingnews': trendingnews,
        'category': category,
        'about': about,
    }
    
    return render(request, 'bookmarks.html', ctx)


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    
    news = News.objects.filter(tags=tag)
    list_news = ListNews.objects.filter(tags=tag)
    trending_news = TrendingNews.objects.filter(tags=tag)
    single_pages = SinglePage.objects.filter(tags=tag)
    
    all_items = list(news) + list(list_news) + list(trending_news) + list(single_pages)
    
    paginator = Paginator(all_items, 10)
    page = request.GET.get('page', 1)
    items = paginator.get_page(page)
    
    trendingnews = TrendingNewsList.objects.all()
    category = Category.objects.all()
    about = SinglePage.objects.first()
    
    ctx = {
        'tag': tag,
        'items': items,
        'trendingnews': trendingnews,
        'category': category,
        'about': about,
    }
    
    return render(request, 'tag_detail.html', ctx)


def featured_news(request):
    featured = []
    
    for item in MainNewsBig.objects.filter(is_featured=True)[:5]:
        featured.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'model_type': 'main_big',
            'id': item.id,
        })
    
    for item in News.objects.filter(is_featured=True)[:5]:
        featured.append({
            'title': item.title,
            'image': item.image,
            'date': item.date,
            'views': item.views,
            'category': item.category,
            'model_type': 'news',
            'id': item.id,
        })
    
    for item in SinglePage.objects.filter(is_featured=True)[:5]:
        featured.append({
            'title': item.title,
            'image': item.image,
            'date': item.created_at,
            'views': item.views,
            'category': item.category,
            'model_type': 'single',
            'id': item.id,
        })
    
    featured.sort(key=lambda x: x['date'], reverse=True)
    
    trendingnews = TrendingNewsList.objects.all()
    category = Category.objects.all()
    about = SinglePage.objects.first()
    
    ctx = {
        'featured': featured,
        'trendingnews': trendingnews,
        'category': category,
        'about': about,
    }
    
    return render(request, 'featured.html', ctx)


def breaking_news(request):
    breaking = MainNewsBig.objects.filter(is_breaking=True).first()
    
    if not breaking:
        breaking = MainNewsBig.objects.first()
    
    trendingnews = TrendingNewsList.objects.all()
    category = Category.objects.all()
    about = SinglePage.objects.first()
    
    ctx = {
        'breaking': breaking,
        'trendingnews': trendingnews,
        'category': category,
        'about': about,
    }
    
    return render(request, 'breaking_news.html', ctx)


def sitemap(request):
    """Generate dynamic sitemap.xml for SEO."""
    from django.http import HttpResponse
    from django.urls import reverse
    from datetime import datetime
    
    # Get all published content
    single_pages = SinglePage.objects.filter(status='published')
    news_items = News.objects.filter(status='published')
    mainnews_items = MainNews.objects.filter(status='published')
    categories = Category.objects.all()

    xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_parts.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Static pages
    static_pages = [
        ('home', '1.0'),
        ('about', '0.8'),
        ('contact', '0.8'),
        ('blog', '0.8'),
        ('technology', '0.8'),
        ('business', '0.8'),
        ('politics', '0.8'),
        ('science', '0.8'),
        ('events', '0.7'),
    ]
    
    for url_name, priority in static_pages:
        try:
            url = request.build_absolute_uri(reverse(url_name))
            xml_parts.append(f'  <url>')
            xml_parts.append(f'    <loc>{url}</loc>')
            xml_parts.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
            xml_parts.append(f'    <changefreq>daily</changefreq>')
            xml_parts.append(f'    <priority>{priority}</priority>')
            xml_parts.append(f'  </url>')
        except:
            pass

    for cat in categories:
        try:
            url = request.build_absolute_uri(reverse('category_detail', kwargs={'slug': cat.slug}))
            xml_parts.append(f'  <url>')
            xml_parts.append(f'    <loc>{url}</loc>')
            xml_parts.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
            xml_parts.append(f'    <changefreq>weekly</changefreq>')
            xml_parts.append(f'    <priority>0.6</priority>')
            xml_parts.append(f'  </url>')
        except:
            pass

    for page in single_pages:
        try:
            url = request.build_absolute_uri(reverse('single', kwargs={'id': page.id}))
            lastmod = page.updated_at.strftime('%Y-%m-%d') if hasattr(page, 'updated_at') and page.updated_at else datetime.now().strftime('%Y-%m-%d')
            xml_parts.append(f'  <url>')
            xml_parts.append(f'    <loc>{url}</loc>')
            xml_parts.append(f'    <lastmod>{lastmod}</lastmod>')
            xml_parts.append(f'    <changefreq>monthly</changefreq>')
            xml_parts.append(f'    <priority>0.9</priority>')
            xml_parts.append(f'  </url>')
        except:
            pass
    
    xml_parts.append('</urlset>')
    
    return HttpResponse('\n'.join(xml_parts), content_type='application/xml')


def robots_txt(request):
    from django.http import HttpResponse
    from django.conf import settings
    import os
    
    robots_path = os.path.join(settings.BASE_DIR, 'static', 'robots.txt')
    try:
        with open(robots_path, 'r') as f:
            content = f.read()
    except:
        content = """User-agent: *
Allow: /
Disallow: /admin/
Sitemap: http://127.0.0.1:8000/sitemap.xml
"""
    
    return HttpResponse(content, content_type='text/plain')


@login_required
def comment_vote(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    comment_id = request.POST.get('comment_id')
    vote_type = request.POST.get('vote_type')
    
    if not comment_id or not vote_type:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)
    
    vote_value = 1 if vote_type == 'like' else -1
    
    existing_vote = CommentVote.objects.filter(user=request.user, comment=comment).first()
    
    if existing_vote:
        if existing_vote.vote == vote_value:
            existing_vote.delete()
            action = 'removed'
        else:
            existing_vote.vote = vote_value
            existing_vote.save()
            action = 'changed'
    else:
        CommentVote.objects.create(user=request.user, comment=comment, vote=vote_value)
        action = 'added'
    
    likes = comment.votes.filter(vote=1).count()
    dislikes = comment.votes.filter(vote=-1).count()
    
    return JsonResponse({
        'success': True,
        'action': action,
        'likes': likes,
        'dislikes': dislikes,
        'total': likes - dislikes
    })


@login_required
def delete_comment(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    comment_id = request.POST.get('comment_id')
    
    if not comment_id:
        return JsonResponse({'error': 'Missing comment_id'}, status=400)
    
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)
    
    if comment.author != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    comment.delete()
    
    return JsonResponse({
        'success': True,
        'message': 'Comment deleted successfully'
    })


@login_required
def telegram_test_send(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Staff access required'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    single_page_id = request.POST.get('single_page_id')
    
    if not single_page_id:
        return JsonResponse({'error': 'Missing single_page_id'}, status=400)
    
    try:
        single_page = SinglePage.objects.get(id=single_page_id)
    except SinglePage.DoesNotExist:
        return JsonResponse({'error': 'Article not found'}, status=404)

    telegram_setting = TelegramSetting.objects.filter(is_active=True).first()
    if not telegram_setting:
        return JsonResponse({'error': 'No active Telegram settings found'}, status=400)
    
    # Build message
    from django.conf import settings
    message = (
        f"🧪 TEST YUBORISH\n\n"
        f"<b>{single_page.title}</b>\n\n"
        f"Bu test xabardir\n\n"
        f"🔗 <a href='{settings.SITE_URL}/single/{single_page.id}/'>Batafsil o'qish</a>"
    )
    
    try:
        from .utils import send_telegram_message, send_telegram_photo
        if single_page.image and single_page.image.url:
            image_url = f"{settings.SITE_URL}{single_page.image.url}"
            result = send_telegram_photo(image_url, message)
        else:
            result = send_telegram_message(message)

        TelegramLog.objects.create(
            news=single_page,
            channel_id=telegram_setting.channel_id,
            status='sent',
            telegram_message_id=str(result.get('message_id', '')) if isinstance(result, dict) else ''
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Test message sent successfully'
        })
    except Exception as e:
        return JsonResponse({
            'error': f'Failed to send: {str(e)}'
        }, status=500)
