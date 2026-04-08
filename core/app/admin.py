from datetime import timedelta
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group as AuthGroup
from django.db.models import Sum, Count
from django.utils import timezone
from django.urls import path
from django.http import JsonResponse, HttpResponse
from django.template.response import TemplateResponse
from unfold.admin import ModelAdmin
from .models import (
    About, Banner, Category, Comment, Event, EventMain, Forum, Group, 
    LikeDislike, ListNews, MainNewsBig, Member, News, 
    NewsletterSubscriber, NewsImage, SinglePage, SocialMedia, Tag, 
    TelegramLog, TelegramSetting, TrendingNews, TrendingNewsList, 
    UserProfile, VideoNews, Bookmark, VerificationCode, CommentVote
)


class CustomAdminSite(AdminSite):
    site_header = "24 News Admin"
    site_title = "Dashboard"
    index_title = "Overview"
    index_template = 'admin/dashboard.html'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('search/', self.admin_view(self.search_view), name='search'),
        ]
        return custom_urls + urls
    
    def search_view(self, request):
        query = request.GET.get('s', '')
        results = []
        
        if query:
            news_results = News.objects.filter(title__icontains=query)[:5]
            single_results = SinglePage.objects.filter(title__icontains=query)[:5]
            
            for item in news_results:
                results.append({
                    'title': item.title,
                    'url': f'/admin/app/news/{item.id}/change/',
                    'type': 'News'
                })
            for item in single_results:
                results.append({
                    'title': item.title,
                    'url': f'/admin/app/singlepage/{item.id}/change/',
                    'type': 'Single Page'
                })
        
        if request.GET.get('extended'):
            html = '<div id="command-results-list">'
            for r in results:
                html += f'<div class="command-result"><a href="{r["url"]}">{r["title"]}</a> <span>{r["type"]}</span></div>'
            html += '</div>'
            return HttpResponse(html)
        
        return JsonResponse({'results': results})
    
    def index(self, request, extra_context=None):
        view_models = [News, SinglePage, MainNewsBig, ListNews, VideoNews]
        all_posts = []
        total_views_sum = 0
        
        for model in view_models:
            posts = model.objects.order_by('-views')[:5]
            total_views_sum += model.objects.aggregate(Sum('views'))['views__sum'] or 0
            for p in posts:
                all_posts.append({
                    'title': p.title,
                    'views': p.views,
                    'type': model._meta.verbose_name.title(),
                    'url': f'/admin/app/{model._meta.model_name}/{p.id}/change/'
                })
        
        all_posts.sort(key=lambda x: x['views'], reverse=True)
        
        most_liked = SinglePage.objects.order_by('-likes')[:10]
        top_liked = [{
            'title': p.title,
            'likes': p.likes,
            'dislikes': p.dislikes,
            'type': 'Single Page',
            'url': f'/admin/app/singlepage/{p.id}/change/'
        } for p in most_liked]
        
        extra_context = extra_context or {}
        extra_context.update({
            'top_posts': all_posts[:10],
            'most_liked': top_liked,
            'total_news': News.objects.count(),
            'total_pages': SinglePage.objects.count(),
            'total_comments': Comment.objects.count(),
            'pending_comments': Comment.objects.filter(is_approved=False).count(),
            'total_views': total_views_sum,
            'total_users': User.objects.count(),
            'recent_users': User.objects.order_by('-date_joined')[:5],
            'most_commented': SinglePage.objects.annotate(
                comment_count=Count('comments')
            ).order_by('-comment_count')[:5],
            'recent_activity': Comment.objects.select_related('author', 'single_page').order_by('-created_at')[:10],
            'news_by_category': Category.objects.annotate(
                news_count=Count('post')
            ).order_by('-news_count'),
            'views_last_week': SinglePage.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=7)
            ).aggregate(total=Sum('views'))['total'] or 0,
        })
        
        context = self.each_context(request)
        context.update(extra_context)
        if 'app_list' not in context:
            context['app_list'] = self.get_app_list(request)
        request.current_app = self.name
        return TemplateResponse(request, 'admin/dashboard.html', context)


admin_site = CustomAdminSite(name='myadmin')


class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ('groups', 'user_permissions')


class GroupAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('permissions',)


class SocialMediaAdmin(ModelAdmin):
    list_display = ('platform', 'url', 'is_active')
    list_filter = ('is_active', 'platform')
    search_fields = ('platform', 'url')


class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)
    ordering = ('name',)


class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    ordering = ('name',)


class NewsAdmin(ModelAdmin):
    list_display = ('title', 'category', 'date', 'views', 'is_featured', 'author')
    list_filter = ('category', 'date', 'is_featured', 'tags')
    search_fields = ('title', 'content')
    date_hierarchy = 'date'
    ordering = ('-date',)
    exclude = ('views',)
    filter_horizontal = ('tags',)


class ListNewsAdmin(ModelAdmin):
    list_display = ('title', 'category', 'date', 'views', 'is_featured', 'author')
    list_filter = ('category', 'date', 'is_featured', 'tags')
    search_fields = ('title', 'content')
    date_hierarchy = 'date'
    ordering = ('-date',)
    exclude = ('views',)
    filter_horizontal = ('tags',)


class MainNewsBigAdmin(ModelAdmin):
    list_display = ('title', 'category', 'date', 'views', 'is_breaking', 'is_featured', 'author')
    list_filter = ('category', 'date', 'is_breaking', 'is_featured', 'tags')
    search_fields = ('title',)
    date_hierarchy = 'date'
    exclude = ('views',)
    filter_horizontal = ('tags',)


class MainNewsAdmin(ModelAdmin):
    list_display = ('title', 'date', 'is_featured', 'author')
    list_filter = ('is_featured', 'tags')
    search_fields = ('title',)
    date_hierarchy = 'date'
    exclude = ('views',)
    filter_horizontal = ('tags',)


class TrendingNewsAdmin(ModelAdmin):
    list_display = ('title', 'category', 'date', 'publisher', 'is_featured', 'author')
    list_filter = ('category', 'is_featured', 'tags')
    search_fields = ('title',)
    exclude = ('views',)
    filter_horizontal = ('tags',)


class TrendingNewsListAdmin(ModelAdmin):
    list_display = ('title', 'date', 'views', 'is_featured', 'author')
    list_filter = ('is_featured', 'tags')
    search_fields = ('title',)
    date_hierarchy = 'date'
    exclude = ('views',)
    filter_horizontal = ('tags',)


class VideoNewsAdmin(ModelAdmin):
    list_display = ('title', 'category', 'date', 'views', 'is_featured', 'author')
    list_filter = ('category', 'date', 'is_featured', 'tags')
    search_fields = ('title',)
    exclude = ('views',)
    filter_horizontal = ('tags',)


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 3


class SinglePageAdmin(ModelAdmin):
    inlines = [NewsImageInline]
    list_display = ('title', 'is_main_page', 'is_about_page', 'category', 'updated_at', 'views', 'author', 'likes', 'dislikes')
    list_filter = ('is_main_page', 'is_about_page', 'category', 'updated_at', 'tags')
    search_fields = ('title', 'description')
    date_hierarchy = 'updated_at'
    ordering = ('-updated_at',)
    exclude = ('views', 'likes', 'dislikes')
    filter_horizontal = ('tags',)


class CommentAdmin(ModelAdmin):
    list_display = ('author', 'content_preview', 'created_at', 'is_approved', 'parent')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('content', 'author__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    actions = ['approve_comments', 'reject_comments']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'
    
    @admin.action(description='Approve selected comments')
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} comments approved.')
    
    @admin.action(description='Reject selected comments')
    def reject_comments(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} comments rejected.')


class BookmarkAdmin(ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    date_hierarchy = 'created_at'


class LikeDislikeAdmin(ModelAdmin):
    list_display = ('user', 'vote_type', 'vote', 'created_at')
    list_filter = ('vote', 'created_at')
    search_fields = ('user__username',)
    
    def vote_type(self, obj):
        return 'Like' if obj.vote == 1 else 'Dislike'
    vote_type.short_description = 'Vote'


class AboutAdmin(ModelAdmin):
    list_display = ('__str__', 'url_in')
    search_fields = ('description',)


class LastlyModifiedAdmin(ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title',)
    date_hierarchy = 'date'
    exclude = ('views',)


class ForumAdmin(ModelAdmin):
    list_display = ('title', 'category', 'date', 'views')
    list_filter = ('category', 'date')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'
    exclude = ('views',)


class ForumGroupAdmin(ModelAdmin):
    list_display = ('name', 'members', 'category', 'date')
    list_filter = ('category', 'date')
    search_fields = ('name', 'description')
    date_hierarchy = 'date'


class MemberAdmin(ModelAdmin):
    list_display = ('name', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('is_active', 'role', 'date_joined')
    search_fields = ('name', 'email', 'bio')
    date_hierarchy = 'date_joined'


class EventAdmin(ModelAdmin):
    list_display = ('title', 'date', 'location', 'category', 'views')
    list_filter = ('category', 'date')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'
    exclude = ('views',)


class UserProfileAdmin(ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'user__email', 'bio')
    raw_id_fields = ('user',)


class TelegramSettingAdmin(ModelAdmin):
    list_display = ('name', 'channel_username', 'is_active', 'test_mode', 'updated_at')
    list_filter = ('is_active', 'test_mode')
    search_fields = ('name', 'channel_username', 'channel_id')


class TelegramLogAdmin(ModelAdmin):
    list_display = ('news', 'status', 'channel_id', 'sent_at', 'retry_count')
    list_filter = ('status', 'sent_at')
    search_fields = ('news__title', 'channel_id', 'error_message')
    readonly_fields = ('sent_at',)
    date_hierarchy = 'sent_at'


class BannerAdmin(ModelAdmin):
    list_display = ('title', 'position', 'is_active', 'order', 'clicks', 'impressions', 'created_at')
    list_filter = ('position', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    search_fields = ('title',)
    date_hierarchy = 'created_at'


class CommentVoteAdmin(ModelAdmin):
    list_display = ('user', 'comment', 'vote_type', 'created_at')
    list_filter = ('vote', 'created_at')
    search_fields = ('user__username', 'comment__content')
    date_hierarchy = 'created_at'
    
    def vote_type(self, obj):
        return 'Like' if obj.vote == 1 else 'Dislike'
    vote_type.short_description = 'Vote'


admin_site.register(Category, CategoryAdmin)
admin_site.register(Tag, TagAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(AuthGroup, GroupAdmin)
admin_site.register(News, NewsAdmin)
admin_site.register(ListNews, ListNewsAdmin)
admin_site.register(MainNewsBig, MainNewsBigAdmin)
admin_site.register(TrendingNews, TrendingNewsAdmin)
admin_site.register(TrendingNewsList, TrendingNewsListAdmin)
admin_site.register(VideoNews, VideoNewsAdmin)
admin_site.register(SinglePage, SinglePageAdmin)
admin_site.register(Comment, CommentAdmin)
admin_site.register(Bookmark, BookmarkAdmin)
admin_site.register(LikeDislike, LikeDislikeAdmin)
admin_site.register(About, AboutAdmin)
admin_site.register(Forum, ForumAdmin)
admin_site.register(Group, ForumGroupAdmin)
admin_site.register(Member, MemberAdmin)
admin_site.register(Event, EventAdmin)
admin_site.register(UserProfile, UserProfileAdmin)
admin_site.register(TelegramSetting, TelegramSettingAdmin)
admin_site.register(TelegramLog, TelegramLogAdmin)
admin_site.register(Banner, BannerAdmin)
admin_site.register(CommentVote, CommentVoteAdmin)
admin_site.register(SocialMedia, SocialMediaAdmin)
