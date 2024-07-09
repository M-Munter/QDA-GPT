# qda_gpt/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Root URL directs to the dashboard
    path('setup-status/', views.get_setup_status, name='setup_status'),  # New path for setup status
    path('clear-session/', views.clear_session, name='clear_session'),  # Add this line
    path('download_csv/', views.download_csv, name='download_csv'),  # For downloading CSV
]