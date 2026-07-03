from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User  
from .models import Complaint, Notice, ComplaintHistory

@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('/admin/')

    if request.method == 'POST' and 'submit_complaint' in request.POST:
        category = request.POST.get('category')
        priority = request.POST.get('priority')
        description = request.POST.get('description')
        photo = request.FILES.get('photo')

        complaint = Complaint.objects.create(
            resident=request.user,
            category=category,
            priority=priority,
            description=description,
            photo=photo
        )
        
        ComplaintHistory.objects.create(
            complaint=complaint,
            status='Open',
            note='Complaint registered successfully.',
            actor=request.user
        )
        
        messages.success(request, "Complaint logged successfully!")
        return redirect('dashboard')

    all_complaints = Complaint.objects.filter(resident=request.user)
    sorted_complaints = sorted(all_complaints, key=lambda c: c.overdue_status(), reverse=True)
    notices = Notice.objects.all().order_by('-is_important', '-created_at')

    context = {
        'complaints': sorted_complaints,
        'notices': notices
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def update_status(request, complaint_id):
    if request.method == 'POST':
        get_object_or_404(Complaint, id=complaint_id)
        new_status = request.POST.get('status')
        note = request.POST.get('note')

        old_status = complaint.status
        complaint.status = new_status
        complaint.save()

        ComplaintHistory.objects.create(
            complaint=complaint,
            status=new_status,
            note=note,
            actor=request.user
        )

        if old_status != new_status:
            send_mail(
                subject=f"Complaint #{complaint.id} Status Updated",
                message=f"Hello {complaint.resident.username},\n\nYour complaint status has been changed to '{new_status}'.\nNote: {note}\n\nRegards,\nSociety Management Board",
                from_email='admin@society.com',
                recipient_list=[complaint.resident.email],
                fail_silently=True
            )

        messages.success(request, f"Ticket #{complaint.id} updated to {new_status}!")
    return redirect('/admin/')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Try another.")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully! Please Sign In.")
        return redirect('login')

    return render(request, 'core/register.html')