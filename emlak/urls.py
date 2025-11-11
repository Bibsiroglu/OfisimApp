# emlak/urls.py

from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ana_sayfa, name='ana_sayfa'),
    path('ilanlar/', views.ilan_listesi, name='ilan_listesi'), 
    path('ilanlar/<int:pk>/', views.ilan_detay, name='ilan_detay'), 
    
    path('musteriler/', views.musteri_listesi, name='musteri_listesi'),
    path('musteriler/<int:pk>/', views.musteri_detay, name='musteri_detay'), 
    
    path('arama/', views.gelismis_arama, name='gelismis_arama'), 
]