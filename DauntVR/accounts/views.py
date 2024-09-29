from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from django.contrib.auth.models import User

@api_view(["GET", "get", "Get"])
def api_login(request):
    if request.method.lower() == "get":
        username = request.GET.get("username")
        password = request.GET.get("password")
        authenticated = authenticate(username=username, password=password)

        if authenticated:
            user = User.objects.get(username=username).id
            data = {
                "status": 200,
                "code": True,
                "playerID": user
            }
            return JsonResponse(data)
        else:
            data = {
                "status": 200,
                "code": False,
                "playerID": -1
            }
            return JsonResponse(data)


def web_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        authenticated = authenticate(username=username, password=password)

        if authenticated:
            print("authenticated")
            #user = User.objects.get(username=username, password=password)
            login(request, authenticated)
            return redirect("dashboard")
        else:
            return redirect("web_login")
    else:
        return render(request, "login.html")
