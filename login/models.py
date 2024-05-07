from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Grade(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment = models.CharField(max_length=100)
    grade = models.FloatField()
    weight = models.FloatField()
