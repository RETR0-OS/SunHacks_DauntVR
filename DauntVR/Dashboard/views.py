from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import status
from .models import GameEntry
import boto3
import json
import markdown
# Create your views here.

configuration_prompt = '''
You are tasked with analyzing user data from a VR-based fear management game called DauntVR, where the goal is to help users overcome their fears. The following metrics are tracked for each session:

Total Time (seconds): The total time the user spent in the scenario. A very low time (below 15 seconds) may indicate stress or frustration, while a very high time (above 50 seconds) may show the need for more practice. A time around 30 seconds indicates good fear management. Decreasing total time (assuming the level is cleared) suggests improved fear management.

Exposure Time (seconds): How long the user took to overcome the initial shock and progress in the scenario. A short time indicates quick adaptation, while a long time may suggest high initial anxiety. However, a very short time (less that 5 seconds) indicates that the user rushed and did not analyse the surroundings well.

Sustain Time (seconds): Time spent managing the fear before taking action. Zero indicates avoidance. Higher values show the user is attempting to manage their anxiety before proceeding. A very low value (below 10 seconds) indicates a rushed approach. 

Overcome Time (seconds): Time it took for the user to take the final step and interact with the fear. Zero indicates the user couldn't take the final step, while non-zero values suggest success in confronting the fear. A very high value indicates that the user has trouble taking the final step. A very low value (below 3 seconds) indicates that the decision might be rushed.

Look Away Time (seconds): Time the user spent looking away from the fear. A high value indicates avoidance, while low or zero suggests direct confrontation.

Level Cleared (True/False): Whether the user successfully completed the scenario.

Goal:

Analyze the last entry of the data and generate an insightful report based on the user’s performance.
Conduct a trend analysis by comparing the last entry with previous data. Provide suggestions and feedback to help users improve their fear management over time.
Tone: The report should be friendly and encouraging, offering practical suggestions for improvement. No graphs or charts, text-based analysis only. Format the text using markdown. Just give the analysis. I don't want context data.
'''

bedrock_client = boto3.client('bedrock-runtime', region_name="us-west-2")




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

            game_entry = GameEntry.objects.create(user=user, totalTime=totalTime, exposureTime=exposureTime, sustainTime=sustainTime, overcomeTime=overcomeTime, lookAwayTime=lookAwayTime, levelCleared=levelCleared)
            game_entry.report = fetch_play_reports(user_id)
            game_entry.save()

            return JsonResponse({"status":status.HTTP_200_OK, "message":"entry added"})

        except User.DoesNotExist:
            return JsonResponse({"status":status.HTTP_404_NOT_FOUND, "message":"user not found"})

@login_required
def dashboard(request):
    game_data = GameEntry.objects.filter(user=request.user).order_by("-id")
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
    md = markdown.Markdown(extensions=["fenced_code"])
    report = md.convert(game.report)

    data ={
        "report_text": report
    }

    return render(request,"showReport.html", context=data)

def fetch_play_reports(user_id):

    past_data = GameEntry.objects.filter(user=User.objects.get(id=user_id)).order_by("id")
    csv_data = ["totalTime, exposureTime, sustainTime, overcomeTime, lookAwayTime, levelCompleted"]

    for data in past_data:
        csv_data.append(f"{data.totalTime},{data.exposureTime},{data.sustainTime},{data.overcomeTime},{data.lookAwayTime},{data.levelCleared}")

    user_data = "Analyse the following game data: \n" + "\n".join(csv_data)


    kwargs = {
        "modelId": "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "messages": [
                {
                    "role": "user",
                    "content": configuration_prompt + "\n" + user_data
                }
            ]
        })
    }
    response = bedrock_client.invoke_model(**kwargs)

    report_data = json.loads(response['body'].read())["content"][0]["text"]
    return report_data
