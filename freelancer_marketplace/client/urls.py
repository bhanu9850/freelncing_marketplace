from client import views
from django.urls import path,include
from django.contrib.auth.views import LogoutView
urlpatterns = [
path('', views.client_home, name='client_home'),
path('login_client/', views.login_client, name='login_client'),
path('register_client/', views.register_client, name='register_client'),
path('logout/', LogoutView.as_view(next_page='client_home'), name='client_logout'),
path('client_dashboard/', views.client_dashboard, name='client_dashboard'),
path('all_freelancers/', views.all_freelancers, name='all_freelancers'),
path('add_project/', views.add_project, name='add_project'),
path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
path('process/<int:project_id>/', views.process_payment, name='process_payment'),
path('confirmation/', views.payment_confirmation, name='payment_confirmation'),

]