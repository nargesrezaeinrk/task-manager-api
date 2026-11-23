from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone
from django.http import JsonResponse

from apps.planner.models import WeeklyPlanner, PlannerCell
from apps.planner.services import create_weekly_planner_service


@login_required
def planner_dashboard(request):
    weekly_planners = WeeklyPlanner.objects.filter(
        user=request.user
    )

    return render(
        request,
        'planner/planner_dashboard.html',
        {'weekly_planners': weekly_planners}
    )


@login_required
@require_POST
def create_weekly_planner_view(request):
    weekly_planner = create_weekly_planner_service(request.user)

    return redirect(
        'weekly_planner_detail',
        pk = weekly_planner.pk,
    )


@login_required
def weekly_planner_detail(request, pk):
    weekly_planner = get_object_or_404(
        WeeklyPlanner,
        pk=pk,
        user=request.user,
    )
    
    days = list(PlannerCell.Day.choices)

    cells_by_position = {
        (cell.day, cell.row_number): cell
        for cell in weekly_planner.cells.all()
    }

    rows = [
        {
            "number": row_number,
            "cells": [
                cells_by_position[(day_code, row_number)]
                for day_code, _ in days
            ],
        }
        for row_number in range(1, 5)
    ]

    older_week = WeeklyPlanner.objects.filter(
        user=request.user,
        created_at__lt=weekly_planner.created_at,
    ).order_by("-created_at").first()

    newer_week = WeeklyPlanner.objects.filter(
        user=request.user,
        created_at__gt=weekly_planner.created_at,
    ).order_by("created_at").first()

    return render(
        request,
        "planner/weekly_planner_detail.html",
        {
            "weekly_planner": weekly_planner,
            "days": days,
            "rows": rows,
            "older_week": older_week,
            "newer_week": newer_week,
        },
    )


@login_required
@require_POST
def save_weekly_planner(request, pk):
    weekly_planner = get_object_or_404(
        WeeklyPlanner,
        pk=pk,
        user=request.user,
    )

    with transaction.atomic():
        cells = weekly_planner.cells.all()
        
        for cell in cells:
            field_name = f"cell_{cell.day}_{cell.row_number}"
            new_content = request.POST.get(field_name, "")

            if cell.content != new_content:
                cell.content = new_content
                cell.updated_at = timezone.now()
                
                cell.save(
                    update_fields=["content", "updated_at"]     
                )
             
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True})
    
    return redirect(
        'weekly_planner_detail',
        pk=weekly_planner.pk,
            
    )
    

@login_required
@require_POST
def delete_weekly_planner(request, pk):
    weekly_planner = get_object_or_404(
        WeeklyPlanner,
        pk=pk,
        user=request.user,
    )
    
    weekly_planner.delete()
    
    return redirect("planner_dashboard")