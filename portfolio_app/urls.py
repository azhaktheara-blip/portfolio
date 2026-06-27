from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/profile/', views.admin_profile, name='admin_profile'),
    path('dashboard/projects/', views.admin_projects, name='admin_projects'),
    path('dashboard/skills/', views.admin_skills, name='admin_skills'),
    path('dashboard/experience/', views.admin_experience, name='admin_experience'),
    path('dashboard/messages/', views.admin_messages_view, name='admin_messages'),
]