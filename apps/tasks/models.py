from dataclasses import fields
from email.policy import default
from django.db import models
from django.conf import settings


class Task(models.Model):
    
    class Status(models.TextChoices):
        TODO = "TODO", "To Do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", 'Completed'

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "tasks",
    )
    
    title = models.CharField(
        max_length=200,
    )
    
    description = models.TextField(
        blank=True,
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )
    
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.LOW,
    )
    
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    labels = models.ManyToManyField(
        "Label",
        blank=True,
        related_name="tasks",    
    )

    def __str__(self):
        return self.title
    

class Label(models.Model):
    name = models.CharField(max_length=100)
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "labels",
    )

    color = models.CharField(max_length=7, default="#7897B8")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["owner", "name"],
                name = "unique_label_per_user"
            )
        ]