from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from apps.user.views import *
from rest_framework_simplejwt import views as jwt_views

router = routers.SimpleRouter()
router.register('api_user', APIUserViewSet,basename='api_user')
urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('me/', GetProfile.as_view(), name='get_profile'),
    path('alter_user_token/', AlterTokenValidityView.as_view(), name='alter_user_token'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
