from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.planner_dashboard,
        name="planner_dashboard",
    ),
    path(
        "create/",
        views.create_weekly_planner_view,
        name="create_weekly_planner",
    ),
    path(
        "week/<int:pk>/",
        views.weekly_planner_detail,
        name="weekly_planner_detail",
    ),
    path(
        "week/<int:pk>/save/",
        views.save_weekly_planner,
        name="save_weekly_planner",
    ),
    path(
        "week/<int:pk>/delete/",
        views.delete_weekly_planner,
        name="delete_weekly_planner",
    ),    
]