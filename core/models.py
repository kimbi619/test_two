from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Person(models.Model):

    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)

    surname = models.CharField(max_length=100)

    initials = models.CharField(max_length=5)

    age = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)]
    )
    
    date_of_birth = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'surname', 'date_of_birth'],
                name='unique_person'
            )
        ]

    def __str__(self):
        return f"{self.name} {self.surname}"
