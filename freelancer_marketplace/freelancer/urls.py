from freelancer import views
from django.urls import path

from django.contrib.auth.views import LogoutView

urlpatterns = [
path('', views.freelancer_home, name='freelancer_home'),
path('login_freelancer/', views.login_freelancer, name='login_freelancer'),
path('register_freelancer/', views.register_freelancer, name='register_freelancer'),
path('freelancer_dashboard/', views.freelancer_dashboard, name='freelancer_dashboard'),
path('all_clients/', views.all_clients, name='all_clients'),
path('all_projects/', views.all_projects, name='all_projects'),
path('logout/', LogoutView.as_view(next_page='freelancer_home'), name='freelancer_logout'),
path('update_project_status/', views.update_project_status, name='update_project_status'),
]