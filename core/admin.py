from django.contrib import admin
from .models import Complaint, ComplaintHistory, Notice

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'resident', 'category', 'priority', 'status', 'created_at', 'is_overdue')
    list_display_links = ('id', 'resident') # Isse ID aur Resident dono par click hone lagega
    list_filter = ('status', 'category', 'priority')
    search_fields = ('description', 'resident__username')
    readonly_fields = ('created_at', 'updated_at')
    
    fields = ('resident', 'category', 'priority', 'status', 'description', 'photo', 'created_at', 'updated_at')

    def is_overdue(self, obj):
        return obj.overdue_status()
    is_overdue.boolean = True
    is_overdue.short_description = "Overdue?"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        all_complaints = Complaint.objects.all()
        
        extra_context['total_open'] = all_complaints.filter(status='Open').count()
        extra_context['total_progress'] = all_complaints.filter(status='In Progress').count()
        extra_context['total_resolved'] = all_complaints.filter(status='Resolved').count()
        extra_context['total_overdue'] = sum(1 for c in all_complaints if c.overdue_status())
        
        extra_context['cat_plumbing'] = all_complaints.filter(category='Plumbing').count()
        extra_context['cat_electrical'] = all_complaints.filter(category='Electrical').count()
        extra_context['cat_lift'] = all_complaints.filter(category='Lift/Elevator').count()
        extra_context['cat_clean'] = all_complaints.filter(category='Cleanliness').count()
        extra_context['cat_others'] = all_complaints.filter(category='Others').count()
        
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(ComplaintHistory)
admin.site.register(Notice)

admin.site.site_header = "Society Maintenance Admin Portal"
admin.site.site_title = "Society Admin"
admin.site.index_title = "Welcome to Management Control Panel!"


from django.utils.safestring import mark_safe

admin.site.site_header = mark_safe('''
    <span style="color: #ffffff !important;">Society Maintenance Admin Portal</span>
    <style>
        .theme-toggle, #theme-toggle, .header-actions, button[id*="theme"], svg.theme-icon {
            display: none !important;
            visibility: hidden !important;
        }

        body {
            background: linear-gradient(135deg, #0b1329 0%, #0f172a 100%) !important;
            color: #f1f5f9 !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            min-height: 100vh;
        }

        #header {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 20px rgba(37, 99, 235, 0.25) !important;
            padding: 18px 30px !important;
            border-bottom: 2px solid #3b82f6 !important;
        }
        #branding h1 { 
            color: #ffffff !important; 
            font-weight: 700 !important; 
            font-size: 20px !important;
        }
        #branding h1 a:link, #branding h1 a:visited {
            color: #ffffff !important;
        }
        #user-tools { 
            color: #e2e8f0 !important; 
            font-size: 13px !important; 
        }
        #user-tools a { 
            color: #ffffff !important; 
            font-weight: 700 !important;
        }

        div.breadcrumbs { 
            background: #0b1329 !important; 
            border-bottom: 1px solid #1e293b !important; 
            color: #94a3b8 !important;
            padding: 12px 30px !important;
        }
        div.breadcrumbs a { color: #3b82f6 !important; font-weight: 600 !important; }

        #content { 
            padding: 30px !important; 
            max-width: 1200px !important; 
            margin: 0 auto !important;
        }
        
        .content h1 {
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 24px !important;
            margin-bottom: 25px !important;
        }

        #content-main {
            float: none !important;
            width: 100% !important;
        }
        
        #content-related {
            float: none !important;
            width: 100% !important;
            margin: 30px 0 0 0 !important;
            position: relative !important;
        }

        .module {
            background: #0f172a !important; 
            border: 1px solid #1e293b !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3) !important;
            overflow: hidden !important;
            margin-bottom: 30px !important;
        }

        .module caption, .module h2 {
            background: #1e3a8a !important;
            color: #ffffff !important; 
            font-weight: 700 !important;
            font-size: 14px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            padding: 14px 20px !important;
            border-bottom: 1px solid #1e293b !important;
        }

        .dashboard .module table th {
            background: #0b1329 !important;
            color: #94a3b8 !important;
            font-weight: 600 !important;
            padding: 12px 16px !important;
        }
        
        tr.row1 { background: #0f172a !important; }
        tr.row2 { background: #141e33 !important; }

        td, th { 
            border-bottom: 1px solid #1e293b !important; 
            padding: 14px 16px !important;
            white-space: nowrap !important;
        }
        
        td a, th a {
            color: #ffffff !important; 
            font-weight: 600 !important;
            font-size: 14px !important;
            text-decoration: none !important;
        }
        td a:hover, th a:hover {
            color: #3b82f6 !important;
        }

        a.addlink { 
            color: #60a5fa !important; 
            font-weight: 700 !important; 
            background: none !important;
            padding-left: 0 !important;
        }
        a.changelink { 
            color: #ffffff !important; 
            font-weight: 700 !important; 
            background: none !important;
            padding-left: 0 !important;
        }
        
        a.addlink::before { content: "➕ " !important; }
        a.changelink::before { content: "✏️ " !important; }

        #content-related .module {
            background: #0f172a !important;
        }
        #content-related h2 {
            color: #ffffff !important;
            background: #1e3a8a !important;
        }
        .sidebar h3 { 
            color: #94a3b8 !important; 
            font-size: 12px !important;
            text-transform: uppercase !important;
            padding: 15px 20px 5px 20px !important;
        }
        ul.actionlist { padding: 0 20px 20px 20px !important; }
        ul.actionlist li {
            color: #cbd5e1 !important; 
            font-size: 13px !important;
            padding: 8px 0 !important;
            border-bottom: 1px solid #1e293b !important;
        }
        ul.actionlist li a {
            color: #60a5fa !important;
            font-weight: 600 !important;
        }
        span.text { color: #94a3b8 !important; font-style: italic !important; }

        ul.actionlist li.addlink, ul.actionlist li.changelink, ul.actionlist li.deletelink {
            background: none !important;
            padding-left: 0 !important;
        }
        ul.actionlist li.addlink::before { content: "➕ " !important; }
        ul.actionlist li.changelink::before { content: "✏️ " !important; }
        ul.actionlist li.deletelink::before { content: "❌ " !important; }
    </style>
''')