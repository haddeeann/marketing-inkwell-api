from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
    })


@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body)
    user = authenticate(username=data.get("email"), password=data.get("password"))

    if user is not None:
        login(request, user)
        return JsonResponse({"message": "Logged in", "user": {"id": user.id, "email": user.email}})
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=401)


@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"message": "Logged out"})


@csrf_exempt
def register_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return JsonResponse({"error": "Username and password required"}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "User already exists"}, status=400)

    user = User.objects.create_user(username=username, password=password)

    return JsonResponse({"message": "User created", "user": {"id": user.id, "username": user.username}})

