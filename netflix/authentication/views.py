from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from django.http import HttpResponseForbidden
from .serializers import UserSerializer
from django.contrib.auth.models import User


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
    return redirect("authentication:splash-screen")



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

def splash_screen(request):
    """Pantalla inicial para seleccionar perfiles."""
    if request.user.is_authenticated:
        profiles = [
            {"name": request.user.username, "avatar": "/static/avatars/nacho.png"}
        ]
        return render(request, "authentication/splash.html", {"profiles": profiles})
    return redirect("authentication:login")


@login_required
def select_profile(request):
    """Autenticar al usuario al seleccionar un perfil."""
    if request.method == "POST":
        username = request.POST.get("username")
        if username == request.user.username:
            return redirect("streaming:home")  # Cambiar a la página principal
    return redirect("authentication:splash-screen")
