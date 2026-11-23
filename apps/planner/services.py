from django.db import transaction

from .models import WeeklyPlanner, PlannerCell


@transaction.atomic
def create_weekly_planner_service(user):
    weekly_planner = WeeklyPlanner.objects.create(
        user=user
    )

    cells = [
        PlannerCell(
            week=weekly_planner,
            day=day,
            row_number=row_number,
        )
        for day, _ in PlannerCell.Day.choices
        for row_number in range(1, 5)
    ]

    PlannerCell.objects.bulk_create(cells)

    return weekly_planner