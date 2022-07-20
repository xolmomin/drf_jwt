from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import UserModelViewSet, LoginApiView

router = DefaultRouter()
router.register('user', UserModelViewSet, 'user')


urlpatterns = [
    path('api/token/', LoginApiView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
