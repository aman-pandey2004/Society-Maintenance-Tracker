from django.contrib import admin
from django.urls import path, include
from django.core.management import call_command
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

try:
    call_command('migrate', interactive=False)
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@society.com', '1234')
        
    if not User.objects.filter(username='resident').exists():
        User.objects.create_user('resident', 'resident@society.com', '1234')
except Exception as e:
    pass

# Custom CSS injection to restore the exact theme shown in 2.png
admin.site.site_header = mark_safe("""
    Society Maintenance Admin Portal
    <style>
        :root {
            --primary: #2563eb !important;
            --secondary: #1e3a8a !important;
            --accent: #00f2fe !important;
            --body-bg: #0b1329 !important;
            --darkened-bg: #0f172a !important;
        }
        #header {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important;
            padding: 15px 40px !important;
        }
        .module h2, .module caption, div.breadcrumbs {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important;
            color: #ffffff !important;
        }
        body, #container, #content {
            background-color: #0b1329 !important;
            color: #f1f5f9 !important;
        }
        .module {
            background: #0f172a !important;
            border: 1px solid #1e293b !important;
            border-radius: 8px !important;
            overflow: hidden !important;
        }
        .module tr.row1, .module tr.row2 {
            background: #0f172a !important;
        }
        .module tr:hover td {
            background: #141e33 !important;
        }
        a:link, a:visited {
            color: #3b82f6 !important;
        }
    </style>
""")
admin.site.site_title = "Admin Core Engine"
admin.site.index_title = "Welcome to Management Control Panel!"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]