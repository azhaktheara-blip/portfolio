from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from . import csv_db

def index(request):
    return render(request, 'portfolio_app/index.html', {
        'profile':    csv_db.get_profile(),
        'projects':   csv_db.get_projects(),
        'skills':     csv_db.get_skills(),
        'experience': csv_db.get_experience(),
    })

@require_POST
def contact(request):
    name    = request.POST.get('name', '').strip()
    email   = request.POST.get('email', '').strip()
    subject = request.POST.get('subject', '').strip()
    body    = request.POST.get('body', '').strip()
    if not (name and email and body):
        return JsonResponse({'ok': False, 'error': 'Please fill in all required fields.'}, status=400)
    csv_db.save_message(name, email, subject, body)
    return JsonResponse({'ok': True, 'message': "Message received! I'll get back to you soon."})

def admin_messages(request):
    return render(request, 'portfolio_app/admin_messages.html', {'messages': csv_db.get_messages()})
