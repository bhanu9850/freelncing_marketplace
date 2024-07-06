from django.urls import path
from messaging_system import views 

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('send_message/<str:receiver_username>/', views.send_message, name='send_message'),
    # path('send_message/', views.send_message, name='send_message_no_receiver'),
]