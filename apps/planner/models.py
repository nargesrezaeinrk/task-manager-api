from django.db import models
from django.conf import settings


class WeeklyPlanner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="weekly_planners",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return f'Weekly Planner id {self.pk} belonging to {self.user}'

    
class PlannerCell(models.Model):
    
    class Day(models.TextChoices):
        MONDAY = 'MON', 'Monday'
        TUESDAY = 'TUE', 'Tuesday'
        WEDNESDAY = 'WED', 'Wednesday'
        THURSDAY = 'THU', 'Thursday'
        FRIDAY = 'FRI', 'Friday'
        SATURDAY = 'SAT', 'Saturday'
        SUNDAY = 'SUN', 'Sunday'
        
    week = models.ForeignKey(
        WeeklyPlanner,
        on_delete=models.CASCADE,
        related_name="cells"
    )
    
    day = models.CharField(
        choices=Day.choices,
        max_length=3,
    )

    row_number=models.PositiveSmallIntegerField()
    
    content = models.TextField(blank=True)

    updated_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["day", "row_number"]

        constraints = [
            models.UniqueConstraint(
                fields=["week", "day", "row_number"],
                name="unique_planner_cell_position",
            ),
            models.CheckConstraint(
                check=models.Q(row_number__gte=1, row_number__lte=4),
                name="planner_cell_row_between_1_and_4",
            ),
        ]
        
    def __str__(self):
        return f"{self.get_day_display()} - Row {self.row_number}"