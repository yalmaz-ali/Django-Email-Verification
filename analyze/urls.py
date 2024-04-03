from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.home, name='home'),
    path('emails/', views.EmailViewSet.as_view(), name='emails'),
    path('emails/<int:pk>/', views.EmailDetail.as_view(), name='email-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
