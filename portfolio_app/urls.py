from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('admin-messages/', views.admin_messages, name='admin_messages'),
]
