from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('admin_dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'portfolio_app/admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required(login_url='/admin-login/')
def admin_dashboard(request):
    return render(request, 'portfolio_app/admin_dashboard.html', {
        'profile':    csv_db.get_profile(),
        'projects':   csv_db.get_projects(),
        'skills':     csv_db.get_skills(),
        'experience': csv_db.get_experience(),
        'messages':   csv_db.get_messages(),
    })

@login_required(login_url='/admin-login/')
def admin_profile(request):
    if request.method == 'POST':
        csv_db.save_profile({
            'name':     request.POST.get('name', ''),
            'title':    request.POST.get('title', ''),
            'tagline':  request.POST.get('tagline', ''),
            'bio':      request.POST.get('bio', ''),
            'email':    request.POST.get('email', ''),
            'phone':    request.POST.get('phone', ''),
            'location': request.POST.get('location', ''),
            'github':   request.POST.get('github', ''),
            'linkedin': request.POST.get('linkedin', ''),
            'twitter':  request.POST.get('twitter', ''),
            'avatar':   request.POST.get('avatar', ''),
        })
        messages.success(request, 'Profile updated successfully!')
        return redirect('admin_profile')
    return render(request, 'portfolio_app/admin_profile.html', {'profile': csv_db.get_profile()})

@login_required(login_url='/admin-login/')
def admin_projects(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        projects = csv_db.get_projects()
        if action == 'add':
            new_id = str(max([int(p['id']) for p in projects], default=0) + 1)
            projects.append({
                'id': new_id,
                'title': request.POST.get('title', ''),
                'description': request.POST.get('description', ''),
                'tech': request.POST.get('tech', ''),
                'demo_url': request.POST.get('demo_url', ''),
                'github_url': request.POST.get('github_url', ''),
                'image': '',
                'featured': request.POST.get('featured', 'false'),
                'category': request.POST.get('category', 'Web'),
            })
            csv_db.write_projects(projects)
            messages.success(request, 'Project added!')
        elif action == 'delete':
            pid = request.POST.get('id')
            projects = [p for p in projects if p['id'] != pid]
            csv_db.write_projects(projects)
            messages.success(request, 'Project deleted!')
        elif action == 'edit':
            pid = request.POST.get('id')
            for p in projects:
                if p['id'] == pid:
                    p['title'] = request.POST.get('title', '')
                    p['description'] = request.POST.get('description', '')
                    p['tech'] = request.POST.get('tech', '')
                    p['demo_url'] = request.POST.get('demo_url', '')
                    p['github_url'] = request.POST.get('github_url', '')
                    p['featured'] = request.POST.get('featured', 'false')
                    p['category'] = request.POST.get('category', 'Web')
            csv_db.write_projects(projects)
            messages.success(request, 'Project updated!')
        return redirect('admin_projects')
    return render(request, 'portfolio_app/admin_projects.html', {'projects': csv_db.get_projects()})

@login_required(login_url='/admin-login/')
def admin_skills(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        skills = csv_db.get_skills()
        if action == 'add':
            skills.append({
                'name': request.POST.get('name', ''),
                'level': request.POST.get('level', '80'),
                'category': request.POST.get('category', 'Other'),
                'icon': request.POST.get('icon', '⚡'),
            })
            csv_db.write_skills(skills)
            messages.success(request, 'Skill added!')
        elif action == 'delete':
            name = request.POST.get('name')
            skills = [s for s in skills if s['name'] != name]
            csv_db.write_skills(skills)
            messages.success(request, 'Skill deleted!')
        elif action == 'edit':
            name = request.POST.get('original_name')
            for s in skills:
                if s['name'] == name:
                    s['name'] = request.POST.get('name', '')
                    s['level'] = request.POST.get('level', '80')
                    s['category'] = request.POST.get('category', '')
                    s['icon'] = request.POST.get('icon', '')
            csv_db.write_skills(skills)
            messages.success(request, 'Skill updated!')
        return redirect('admin_skills')
    return render(request, 'portfolio_app/admin_skills.html', {'skills': csv_db.get_skills()})

@login_required(login_url='/admin-login/')
def admin_experience(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        experience = csv_db.get_experience()
        if action == 'add':
            new_id = str(max([int(e['id']) for e in experience], default=0) + 1)
            experience.append({
                'id': new_id,
                'company': request.POST.get('company', ''),
                'role': request.POST.get('role', ''),
                'period': request.POST.get('period', ''),
                'description': request.POST.get('description', ''),
                'current': request.POST.get('current', 'false'),
            })
            csv_db.write_experience(experience)
            messages.success(request, 'Experience added!')
        elif action == 'delete':
            eid = request.POST.get('id')
            experience = [e for e in experience if e['id'] != eid]
            csv_db.write_experience(experience)
            messages.success(request, 'Experience deleted!')
        elif action == 'edit':
            eid = request.POST.get('id')
            for e in experience:
                if e['id'] == eid:
                    e['company'] = request.POST.get('company', '')
                    e['role'] = request.POST.get('role', '')
                    e['period'] = request.POST.get('period', '')
                    e['description'] = request.POST.get('description', '')
                    e['current'] = request.POST.get('current', 'false')
            csv_db.write_experience(experience)
            messages.success(request, 'Experience updated!')
        return redirect('admin_experience')
    return render(request, 'portfolio_app/admin_experience.html', {'experience': csv_db.get_experience()})

@login_required(login_url='/admin-login/')
def admin_messages_view(request):
    if request.method == 'POST' and request.POST.get('action') == 'delete':
        idx = int(request.POST.get('index', -1))
        msgs = csv_db.get_messages()
        if 0 <= idx < len(msgs):
            msgs.pop(idx)
            csv_db.write_messages(msgs)
            messages.success(request, 'Message deleted!')
        return redirect('admin_messages')
    return render(request, 'portfolio_app/admin_messages.html', {'messages': csv_db.get_messages()})