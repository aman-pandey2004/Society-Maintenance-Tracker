from django.contrib import admin
from django.urls import path, include
from django.core.management import call_command
from django.contrib.auth.models import User

try:
    call_command('migrate', interactive=False)
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@society.com', '1234')
        
    if not User.objects.filter(username='resident').exists():
        User.objects.create_user('resident', 'resident@society.com', '1234')
except Exception as e:
    pass

# Admin panel par back to resident portal ka link jodne ke liye
admin.site.site_header = "Society Care Operations Panel"
admin.site.site_title = "Admin Core Engine"
admin.site.index_title = "Welcome to Matrix Operations Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]