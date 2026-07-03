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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]