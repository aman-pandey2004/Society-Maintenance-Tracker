from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('Plumbing', 'Plumbing'),
        ('Electrical', 'Electrical'),
        ('Lift/Elevator', 'Lift Issues'),
        ('Cleanliness', 'Garbage / Waste Management'),
        ('Others', 'Others'),
    ]
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    resident = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    description = models.TextField()
    photo = models.ImageField(upload_to='complaints/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def overdue_status(self):
        if self.status != 'Resolved':
            delta = timezone.now() - self.created_at
            return delta.days >= 5
        return False

    def __str__(self):
        return f"{self.category} - {self.resident.username} ({self.status})"

class ComplaintHistory(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.complaint.id} changed to {self.status} at {self.timestamp}"

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail

@receiver(post_save, sender=Notice)
def notify_residents_important_notice(sender, instance, created, **kwargs):
    if created and instance.is_important:
        residents_emails = User.objects.filter(is_staff=False).values_list('email', flat=True)
        active_emails = [email for email in residents_emails if email]
        
        if active_emails:
            send_mail(
                subject=f"📢 Important Notice: {instance.title}",
                message=f"Hello Resident,\n\nA new urgent announcement has been posted on the Society Board:\n\n---\n{instance.content}\n---\n\nPlease log in to your portal to view complete details.\n\nRegards,\nSociety Management Board",
                from_email='admin@society.com',
                recipient_list=active_emails,
                fail_silently=True
            )

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Complaint, ComplaintHistory

@receiver(post_save, sender=Complaint)
def auto_track_complaint_status(sender, instance, created, **kwargs):
    if not created:
        # CORRECT SYNTAX: order_by use hoga bina system crash kiye
        last_log = ComplaintHistory.objects.filter(complaint=instance).order_by('-timestamp').first()
        
        if not last_log or last_log.status != instance.status:
            note_mapping = {
                'In Progress': "Technician assigned, replacement parts dispatched.",
                'Resolved': "Maintenance issue successfully resolved and verified by staff.",
                'Open': "Complaint state re-opened for review."
            }
            final_note = note_mapping.get(instance.status, f"Status transitioned to {instance.status}.")
            
            ComplaintHistory.objects.create(
                complaint=instance,
                status=instance.status,
                note=final_note,
                actor=instance.resident
            )