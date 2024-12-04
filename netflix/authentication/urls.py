from django.urls import path
from .views import CustomLoginView, register, logout_view, my_account, UserProfileView

app_name = "authentication"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", register, name="register"),
    path("logout/", logout_view, name="logout"),
    path("my_account/", my_account, name="my_account"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
]
