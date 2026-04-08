from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Make a user an admin (superuser and staff)'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to make admin')
        parser.add_argument('--email', type=str, help='Email address (optional)')

    def handle(self, *args, **options):
        username = options['username']
        email = options.get('email')
        
        try:
            if email:
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={'email': email}
                )
            else:
                user = User.objects.get(username=username)
            
            user.is_staff = True
            user.is_superuser = True
            user.save()
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created user "{username}" and made them admin')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'User "{username}" is now an admin')
                )
                
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist. Use --email to create.')
            )
