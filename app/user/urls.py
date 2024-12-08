from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import CreateUserView, ManageUserView

app_name = "user"

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create"),
    path("me/", ManageUserView.as_view(), name="me"),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", jwt_views.TokenVerifyView.as_view(), name="token_verify"),
]
