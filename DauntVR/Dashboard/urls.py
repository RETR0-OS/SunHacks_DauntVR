from django.urls import path, include
from .views import add_user_data, dashboard, get_chart_data, get_game_report

urlpatterns = [
    path('add/<int:user_id>', add_user_data, name="api_addUserData"),
    path('dashboard/', dashboard, name='dashboard'),
    path('api/chart/data/', get_chart_data, name='chart_data'),
    path('dashboard/showreport/<int:pk>', get_game_report, name="game_report"),
]
