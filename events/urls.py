from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_list, name='events_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
]