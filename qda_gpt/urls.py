# qda_gpt/urls.py
from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),  # Root URL directs to the dashboard
    path('setup-status/', views.get_setup_status, name='setup_status'),  # New path for setup status
    path('clear-session/', views.clear_session, name='clear_session'),  # Add this line
    path('download_xlsx/', views.download_xlsx, name='download_xlsx'),  # For downloading Excel
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]
