# 📰 24 News - Django News Portal

A full-featured news and content management system built with Django, featuring multilingual support, social authentication, Telegram bot integration, and a modern admin dashboard.

## ✨ Features

### Core Features
- 📝 **Multi-model Content Management** - News, Video News, Trending News, List News, Single Pages
- 🌍 **Multilingual Support** - 6 languages (English, German, French, Spanish, Uzbek, Russian)
- 🔐 **Authentication** - Traditional login/register + Google OAuth via django-allauth
- 💬 **Comments System** - Nested comments with approval workflow and voting
- 🔖 **Bookmarks** - Save favorite articles
- 👍 **Like/Dislike System** - For both articles and comments
- 📧 **Newsletter** - Email subscription with verification
- 🤖 **Telegram Integration** - Auto-post articles to Telegram channels
- 🎨 **Unfold Admin** - Modern, customizable dark-mode admin dashboard
- 📊 **Admin Dashboard** - Analytics with charts, top posts, recent activity

### Content Types
| Model | Description |
|-------|-------------|
| `MainNewsBig` | Hero section news with breaking/featured flags |
| `MainNews` | Standard news articles |
| `News` | Detailed news with rich content |
| `VideoNews` | YouTube/Vimeo video news |
| `ListNews` | List-style news articles |
| `TrendingNews` | Trending stories |
| `SinglePage` | Static pages (About, Contact, etc.) |
| `Banner` | Advertisements with impression tracking |

### SEO & Performance
- Dynamic `sitemap.xml` generation
- `robots.txt` configuration
- Meta tags for social sharing (Open Graph, Twitter Cards)
- Redis caching
- Pagination for all listing pages

## 🛠️ Technology Stack

| Category | Technologies |
|----------|--------------|
| Backend | Django 5.2, Python 3.10+ |
| Database | SQLite (default) / PostgreSQL (recommended) |
| Cache | Redis + django-redis |
| Authentication | django-allauth, Google OAuth |
| Admin UI | django-unfold |
| Frontend | Bootstrap 4, jQuery, Owl Carousel |
| Rate Limiting | django-ratelimit |
| Async Tasks | Django Signals |
| Email | SMTP (Gmail) |
| APIs | Telegram Bot API |

## 📋 Prerequisites

- Python 3.10 or higher
- Redis server (for caching)
- Telegram Bot Token (for auto-posting)
- Google OAuth credentials (for social login)
- Gmail account (for email notifications)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/24-News-Django.git
cd 24-News-Django
2. Create Virtual Environment
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
pip install django
pip install django-allauth
pip install django-redis
pip install django-ratelimit
pip install django-unfold
pip install python-dotenv
pip install Pillow
pip install redis
pip install requests
Or use requirements.txt:

bash
pip install -r requirements.txt
4. Environment Configuration
Create a .env file in the project root:

env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id
5. Database Setup
bash
python manage.py makemigrations
python manage.py migrate
6. Create Superuser
bash
python manage.py createsuperuser
7. Collect Static Files
bash
python manage.py collectstatic
8. Run Development Server
bash
python manage.py runserver
Access the site at http://127.0.0.1:8000
Admin panel at http://127.0.0.1:8000/admin/

📁 Project Structure
text
24-News-Django/
├── core/                   # Project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL routing
│   ├── admin.py            # Custom admin site
│   └── wsgi.py
├── app/                    # Main application
│   ├── models.py           # All database models
│   ├── views.py            # All view functions
│   ├── admin.py            # ModelAdmin configurations
│   ├── urls.py             # App URL patterns
│   ├── signals.py          # Post-save signals (Telegram)
│   └── utils.py            # Helper functions
├── templates/              # HTML templates
│   ├── admin/              # Custom admin templates
│   ├── includes/           # Reusable components
│   ├── index.html          # Homepage
│   ├── single.html         # Article detail
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   └── ...
├── static/                 # CSS, JS, images
├── media/                  # User-uploaded files
├── locale/                 # Translation files
└── manage.py
🔧 Configuration
Telegram Auto-Posting
Create a Telegram Bot via @BotFather

Get your bot token and channel/chat ID

Add to .env file

Configure TelegramSetting in admin panel

When a SinglePage with status 'published' is saved, it auto-posts to Telegram

Google OAuth Setup
Go to Google Cloud Console

Create a new project or select existing

Enable Google+ API

Create OAuth 2.0 credentials

Add Authorized redirect URI: http://127.0.0.1:8000/accounts/google/login/callback/

Add credentials to Django admin under Social applications

Email Configuration
For Gmail SMTP:

Use App Password (not regular password)

Enable 2FA on Google account

Generate app password from Google Account settings

🌐 Internationalization
Translation files are stored in locale/ directory. To add translations:

bash
python manage.py makemessages -l uz  # Uzbek
python manage.py compilemessages
Supported languages: English (en), German (de), French (fr), Spanish (es), Uzbek (uz), Russian (ru)

🔄 Key Workflows
Article Publishing
Create/Edit a SinglePage in admin

Set status to 'published'

Signal triggers Telegram auto-post

Article appears on homepage and category pages

User Interaction
Comments: Logged-in users can comment (rate-limited)

Votes: Like/dislike articles and comments

Bookmarks: Save favorite content

Profile: Customizable user profiles with avatars

📊 Admin Dashboard Features
Real-time statistics (views, users, comments)

Most viewed posts (last 7 days)

Most liked/disliked content

Recent users and activity

Content distribution pie chart

Quick search across all content types

🔐 Security Features
CSRF protection enabled

Rate limiting on login/registration/comments

Session-based authentication

Password validation rules

X-Frame-Options protection

🚢 Deployment
Production Settings
Update settings.py:

python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Use PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
Deploy to Production (Example: Gunicorn + Nginx)
bash
pip install gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000
📝 API Endpoints
Endpoint	Method	Description
/	GET	Homepage
/single/<id>/	GET	Article detail
/search/	GET	Search with filters
/comment/add/	POST	Add comment
/vote/	POST	Like/dislike
/bookmark/toggle/	POST	Toggle bookmark
/comment/vote/	POST	Vote on comment
/sitemap.xml	GET	SEO sitemap
/robots.txt	GET	Robots directives
🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit changes (git commit -m 'Add amazing feature')

Push to branch (git push origin feature/amazing-feature)

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👥 Authors
ExoNiteVX- Initial work

🙏 Acknowledgments
FreeHTML5.co for the original template design

Django Unfold for the modern admin theme

django-allauth team for social authentication

📞 Support
For issues or questions, please open an issue on GitHub or contact the maintainers.

⭐ Star this repository if you find it useful!
