# qda_gpt/urls.py
from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),  # Root URL directs to the dashboard
    path('analysis-status/', views.get_analysis_status, name='analysis_status'),  # New path for setup status
    path('clear-session/', views.clear_session, name='clear_session'),  # Add this line
    path('download_xlsx/', views.download_xlsx, name='download_xlsx'),  # For downloading Excel
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('run_analysis/', views.run_analysis_view, name='run_analysis'),  # Ensure this line is included
    path('update-session/', views.update_session, name='update_session'),  # New path for updating session data
]

