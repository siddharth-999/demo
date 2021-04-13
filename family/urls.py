from django.urls import path
from rest_framework import routers

from .views import LoginAPIView, UserViewSet, FamilyRelativeViewSet

app_name = 'family'

router = routers.DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('family_relative', FamilyRelativeViewSet,
                basename='family_relative')

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
]
urlpatterns += router.urls
