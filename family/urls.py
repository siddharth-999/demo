from django.urls import path
from rest_framework import routers

from .views import LoginAPIView, UserViewSet

app_name = 'family'

router = routers.DefaultRouter()
router.register('user', UserViewSet, basename='user')

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
]
urlpatterns += router.urls
