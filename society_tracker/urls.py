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
    <span style="color: #ffffff; font-weight: 700;">🟢 Society Care Operations Terminal</span>
    <style>
        :root, [data-theme="dark"], [data-theme="light"] {
            --primary: #10b981 !important;
            --secondary: #1f2937 !important;
            --accent: #059669 !important;
            --body-bg: #090d16 !important;
            --body-fg: #ffffff !important;
            --border-color: #374151 !important;
            --darkened-bg: #111827 !important;
        }
        .theme-toggle, #theme-toggle, .header-actions button, button[dir="ltr"] {
            display: none !important;
            visibility: hidden !important;
        }
        #header {
            background: #111827 !important;
            border-bottom: 2px solid #10b981 !important;
            padding: 15px 40px !important;
        }
        #header a { color: #ffffff !important; }
        .module h2, .module caption, div.breadcrumbs {
            background: #1f2937 !important;
            color: #10b981 !important;
            font-weight: 600 !important;
            border-bottom: 1px solid #374151 !important;
        }
        body, #container, #content {
            background-color: #090d16 !important;
            color: #ffffff !important;
        }
        .module {
            background: #111827 !important;
            border: 1px solid #1f2937 !important;
            border-radius: 8px !important;
        }
        .module tr.row1, .module tr.row2 { background: #111827 !important; }
        .module td, .module th {
            border-bottom: 1px solid #1f2937 !important;
            color: #ffffff !important;
        }
        .module tr:hover td { background: #1f2937 !important; }
        a:link, a:visited { color: #10b981 !important; }
    </style>
""")
admin.site.site_title = "Operations Engine"
admin.site.index_title = "System Control Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]