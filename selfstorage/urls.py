from django.urls import path

from .views import index, about, contact, season_storage, order

urlpatterns = [
    path('', index, name='index'),
    path('season', season_storage, name='season_storage'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('order', order, name='order')
]