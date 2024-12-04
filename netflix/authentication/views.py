from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserSerializer


# Vista para iniciar sesión
class CustomLoginView(LoginView):
    template_name = "authentication/login.html"


# Vista para registrar nuevos usuarios
def register(request):
    """Registro de nuevos usuarios."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("authentication:login")
    else:
        form = UserCreationForm()
    return render(request, "authentication/register.html", {"form": form})


# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect("streaming:home")


# Vista para la cuenta de usuario
@login_required
def my_account(request):
    """Muestra la cuenta del usuario."""
    return render(request, "authentication/my_account.html")


# API para el perfil de usuario
class UserProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        data = request.data
        profile = user.profile
        profile.bio = data.get("bio", profile.bio)
        profile.birth_date = data.get("birth_date", profile.birth_date)
        if "avatar" in request.FILES:
            profile.avatar = request.FILES["avatar"]
        profile.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
