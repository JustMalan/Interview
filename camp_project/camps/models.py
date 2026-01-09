from django.db import models


class Camp(models.Model):
    name = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ["start_date", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.start_date} to {self.end_date})"


class ParentRegistration(models.Model):
    parent_name = models.CharField(max_length=120)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.parent_name} <{self.email}>"


class Student(models.Model):
    parent_registration = models.OneToOneField(
        ParentRegistration,
        on_delete=models.CASCADE,
        related_name="student",
    )
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    age = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class CampRegistration(models.Model):
    DURATION_CHOICES = [
        (1, "1 week"),
        (2, "2 weeks"),
    ]

    parent_registration = models.ForeignKey(
        ParentRegistration,
        on_delete=models.CASCADE,
        related_name="camp_registrations",
    )
    camp = models.ForeignKey(
        Camp,
        on_delete=models.CASCADE,
        related_name="registrations",
    )
    duration_weeks = models.PositiveSmallIntegerField(
        choices=DURATION_CHOICES, default=2
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        # prevents duplicate registration per camp
        constraints = [
            models.UniqueConstraint(
                fields=["parent_registration", "camp"],
                name="unique_parent_per_camp",
            )
        ]

    def __str__(self) -> str:
        return f"{self.parent_registration} -> {self.camp} ({self.duration_weeks}w)"
