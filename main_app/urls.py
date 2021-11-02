from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('about/', views.about, name='about'),

    path('finchs/', views.finchs_index, name='index'),
    path('finchs/<int:finch_id>', views.finchs_detail, name='detail'),
]