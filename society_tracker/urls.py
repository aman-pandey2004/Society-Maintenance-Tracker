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
    <span style="color: #ffffff; font-weight: 700;">🏢 Society Care Operations Panel</span>
    <style>
        /* Admin Main Navbar Layout override */
        #header, .navbar-custom, .module h2, .visual-island {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important;
            color: #ffffff !important;
        }
        div.breadcrumbs {
            background: #1e293b !important;
            color: #cbd5e1 !important;
        }
        /* Buttons, text indicators layout links override */
        .module th, .module caption, #content-main h2 {
            background: #0f172a !important;
            color: #94a3b8 !important;
        }
        a:link, a:visited {
            color: #3b82f6 !important;
        }
        /* Dashboard background panel alignment correction */
        body, #content {
            background: #0b1329 !important;
            color: #f1f5f9 !important;
        }
        .module, .app-header {
            background: #0f172a !important;
            border: 1px solid #1e293b !important;
        }
    </style>
""")
admin.site.site_title = "Admin Core Engine"
admin.site.index_title = "Welcome to Operations Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]