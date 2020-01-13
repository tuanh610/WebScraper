from django.urls import path
from . import views

app_name = 'mobile'
urlpatterns = [
    path('', views.home, name='home'),
    path('new_search/', views.new_search, name='new_search'),
    path('all_mobiles/?source=<str:source>&page=<int:page>', views.all_mobiles, name='all_mobiles'),
]
