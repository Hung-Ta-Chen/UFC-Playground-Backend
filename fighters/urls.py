from django.urls import path
from . import views

urlpatterns = [
    path('fighters/', views.fighter_list, name='fighter_list'),
    path('fighters/<int:fighter_id>/', views.fighter_detail, name='fighter_detail'),
    path('predict/', views.predict_match, name='predict_match'),
]