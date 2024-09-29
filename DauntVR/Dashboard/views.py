from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import status
from .models import GameEntry
# Create your views here.

@api_view(["Get", "GET", "get"])
def add_user_data(request, user_id):
    if request.method.lower() == "get":
        try:
            user = User.objects.get(id = user_id)
            totalTime = request.GET.get("totalTime")
            exposureTime = request.GET.get("exposureTime")
            sustainTime = request.GET.get("sustainTime")
            overcomeTime = request.GET.get("overcomeTime")
            lookAwayTime =  request.GET.get("lookAwayTime")
            levelCleared = request.GET.get("levelCleared")

            game_entry = GameEntry(user=user, totalTime=totalTime, exposureTime=exposureTime, sustainTime=sustainTime, overcomeTime=overcomeTime, lookAwayTime=lookAwayTime, levelCleared=levelCleared)
            game_entry.save()

            return JsonResponse({"status":status.HTTP_200_OK, "message":"entry added"})

        except User.DoesNotExist:
            return JsonResponse({"status":status.HTTP_404_NOT_FOUND, "message":"user not found"})

@login_required
def dashboard(request):
    game_data = GameEntry.objects.filter(user=request.user).order_by("id")
    data = {
        "games": game_data,
    }
    return render(request, "dashboard.html", context=data)

@login_required
def get_chart_data(request):
    entries = GameEntry.objects.filter(user=request.user).order_by('id')
    return JsonResponse({
        'labels': list(range(1, len(entries) + 1)),
        'totalTime': [entry.totalTime for entry in entries],
        'exposureTime': [entry.exposureTime for entry in entries],
        'sustainTime': [entry.sustainTime for entry in entries],
        'overcomeTime': [entry.overcomeTime for entry in entries],
        'lookAwayTime': [entry.lookAwayTime for entry in entries],
    })

@login_required
def get_game_report(request, pk):
    game = GameEntry.objects.get(user=request.user, id=pk)
    report = game.report

    data ={
        "report_text": report
    }

    return render(request,"showReport.html", context=data)