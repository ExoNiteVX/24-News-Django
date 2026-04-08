from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)


    class Meta:
        verbose_name_plural = 'Categories'


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)



    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class MainNewsBig(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='MainNewsBig/')
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    is_breaking = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='main_news_big')
    tags = models.ManyToManyField(Tag, blank=True, related_name='main_news_big')

    def __str__(self):
        return self.title


class MainNews(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='MainNews/')
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='main_news')
    tags = models.ManyToManyField(Tag, blank=True, related_name='main_news')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title

class TrendingNews(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='TrendingNews/')
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    publisher = models.CharField(max_length=200, blank=True)
    views = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='trending_news')
    tags = models.ManyToManyField(Tag, blank=True, related_name='trending_news')

    def __str__(self):
        return self.title


class News(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='TrendingNews/')
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='news')
    tags = models.ManyToManyField(Tag, blank=True, related_name='news')
    content = models.TextField(max_length=50000, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title


class VideoNews(models.Model):
    title = models.CharField(max_length=200)
    video = models.URLField(max_length=800)
    image = models.ImageField(upload_to='VideoNews/')
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='video_news')
    tags = models.ManyToManyField(Tag, blank=True, related_name='video_news')

    def __str__(self):
        return self.title


class ListNews(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ListNews/')
    date = models.DateTimeField(auto_now_add=True)
    publisher = models.CharField(max_length=200)
    content = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='list_news')
    tags = models.ManyToManyField(Tag, blank=True, related_name='list_news')

    def __str__(self):
        return self.title

class TrendingNewsList(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='TrendingNewsList/')
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='trending_news_list')
    tags = models.ManyToManyField(Tag, blank=True, related_name='trending_news_list')

    def __str__(self):
        return self.title



class SinglePage(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='SinglePage/')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='post', blank=True, null=True)
    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=50000)
    views = models.PositiveIntegerField(default=0)
    is_main_page = models.BooleanField(default=False)
    is_about_page = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='single_pages')
    tags = models.ManyToManyField(Tag, blank=True, related_name='single_pages')
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    @property
    def reading_time(self):
        words = len(self.description.split())
        return max(1, round(words / 200))


class About(models.Model):
    description = models.TextField(max_length=50000)
    url_in = models.URLField()
    url_google = models.URLField()
    url_facebook = models.URLField()
    url_twitter = models.URLField()

    def __str__(self):
        return f"About Page (ID: {self.id}) - {self.description[:50]}..."


class LastlyModified(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='LastlyModified/')
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Forum(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='Forums/')
    date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class Group(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='Groups/')
    date = models.DateTimeField(auto_now_add=True)
    members = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    bio = models.TextField(max_length=500)
    image = models.ImageField(upload_to='Members/')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=100, default='Member')

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    image = models.ImageField(upload_to='Events/')
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

class EventMain(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    image = models.ImageField(upload_to='Events/')
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class VerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=100, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.code}"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class Comment(models.Model):
    single_page = models.ForeignKey(SinglePage, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    list_news = models.ForeignKey(ListNews, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    trending_news = models.ForeignKey(TrendingNews, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    single_page = models.ForeignKey(SinglePage, on_delete=models.CASCADE, related_name='bookmarked_by', null=True, blank=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='bookmarked_by', null=True, blank=True)
    list_news = models.ForeignKey(ListNews, on_delete=models.CASCADE, related_name='bookmarked_by', null=True, blank=True)
    trending_news = models.ForeignKey(TrendingNews, on_delete=models.CASCADE, related_name='bookmarked_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'single_page', 'news', 'list_news', 'trending_news']

    def __str__(self):
        return f"Bookmark by {self.user.username}"


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTE_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    single_page = models.ForeignKey(SinglePage, on_delete=models.CASCADE, related_name='votes', null=True, blank=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='votes', null=True, blank=True)
    list_news = models.ForeignKey(ListNews, on_delete=models.CASCADE, related_name='votes', null=True, blank=True)
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'single_page', 'news', 'list_news']

    def __str__(self):
        vote_type = 'Like' if self.vote == self.LIKE else 'Dislike'
        return f"{vote_type} by {self.user.username}"


class TelegramLog(models.Model):
    STATUS_CHOICES = (
        ('sent', 'Sent'),
        ('error', 'Error'),
        ('retry', 'Retry'),
    )
    
    news = models.ForeignKey(SinglePage, on_delete=models.CASCADE, related_name='telegram_logs')
    channel_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    error_message = models.TextField(blank=True)
    telegram_message_id = models.CharField(max_length=100, blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    retry_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"Telegram {self.status} for {self.news.title[:30]}..."



class TelegramSetting(models.Model):
    name = models.CharField(max_length=100, default='Default')
    bot_token = models.CharField(max_length=200)
    channel_id = models.CharField(max_length=100)
    channel_username = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    post_format = models.TextField(blank=True)
    test_mode = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Telegram Settings'
    
    def __str__(self):
        return f"{self.name} ({self.channel_username or self.channel_id})"
    
    def save(self, *args, **kwargs):
        if self.is_active:
            TelegramSetting.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)



class Banner(models.Model):
    POSITION_CHOICES = (
        ('home_top', 'Home Page Top'),
        ('home_sidebar', 'Home Page Sidebar'),
        ('article_top', 'Article Page Top'),
        ('article_sidebar', 'Article Page Sidebar'),
        ('footer', 'Footer'),
        ('popup', 'Popup'),
    )
    
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, default='home_top')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['position', 'order', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.position})"
    
    def is_visible(self):
        from django.utils import timezone
        now = timezone.now()
        if not self.is_active:
            return False
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True


class NewsImage(models.Model):
    news = models.ForeignKey(SinglePage, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='news_gallery/')
    caption = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"Image for {self.news.title}"


class CommentVote(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTE_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_votes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='votes')
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'comment']
        ordering = ['-created_at']
    
    def __str__(self):
        vote_type = 'Like' if self.vote == self.LIKE else 'Dislike'
        return f"{vote_type} on comment by {self.user.username}"


class SocialMedia(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter/X'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
    ]
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    url = models.URLField()
    is_active = models.BooleanField(default=True)
    icon_class = models.CharField(max_length=50, blank=True, help_text="Font awesome icon class (e.g., fa-facebook)")
    
    class Meta:
        verbose_name_plural = "Social Media Links"
    
    def __str__(self):
        return self.get_platform_display()
    
    def save(self, *args, **kwargs):
        if not self.icon_class:
            icon_map = {
                'facebook': 'fa-facebook',
                'twitter': 'fa-twitter',
                'instagram': 'fa-instagram',
                'linkedin': 'fa-linkedin',
                'youtube': 'fa-youtube',
                'telegram': 'fa-telegram',
                'whatsapp': 'fa-whatsapp',
            }
            self.icon_class = icon_map.get(self.platform, 'fa-link')
        super().save(*args, **kwargs)