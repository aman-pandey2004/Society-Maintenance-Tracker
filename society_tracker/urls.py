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

admin.site.site_header = mark_safe("""
    Society Maintenance Admin Portal
    <style>
        :root, [data-theme="dark"], [data-theme="light"], html, body {
            --primary: #2563eb !important;
            --secondary: #1e3a8a !important;
            --accent: #00f2fe !important;
            --body-bg: #0b1329 !important;
            --body-fg: #f1f5f9 !important;
            --border-color: #1e293b !important;
            --darkened-bg: #0f172a !important;
            background-color: #0b1329 !important;
            color: #f1f5f9 !important;
        }
        
        .theme-toggle, #theme-toggle, .header-actions, .theme-toggle-wrapper, button[dir="ltr"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
        }
        
        #header {
            background: #2563eb !important;
            padding: 18px 40px !important;
        }
        
        #header a {
            color: #ffffff !important;
        }
        
        .module h2, .module caption, div.breadcrumbs {
            background: #1e3a8a !important;
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        
        .module {
            background: #0f172a !important;
            border: 1px solid #1e293b !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 25px rgba(0,0,0,0.4) !important;
            margin-bottom: 25px !important;
        }
        
        .module tr.row1, .module tr.row2 {
            background: #0f172a !important;
        }
        
        .module td, .module th {
            border-bottom: 1px solid #1e293b !important;
            color: #ffffff !important;
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