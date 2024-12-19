from django.db import models
from datetime import datetime


class Sponsor(models.Model):
    SPONSOR_CHOICES = (
        ("legal_entity", "yuridik shaxs"),
        ("natural_person", "jismoniy shaxs"),
    )
    STATUS_CHOICES = (
        ("new", "yangi"),
        ("moderation", "moderatsiya"),
        ("confirmed", "tasdiqlangan"),
        ("canceled", "bekor qilingan"),
    )

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    amount = models.FloatField()
    sponsor_type = models.CharField(choices=SPONSOR_CHOICES, default="yuridik shaxs",  max_length=100)
    status = models.CharField(choices=STATUS_CHOICES, default="yangi", max_length=100)
    organization = models.CharField(blank=True, null=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class University(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    STUDENT_CHOICES = (
        ("bachelor", "bachelor"),
        ("master", "master"),
    )
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    student_type = models.CharField(choices=STUDENT_CHOICES, default="bachelor", max_length=100)
    student_fee = models.FloatField()
    university = models.ForeignKey(University, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class StudentSponsor(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    allocated_money = models.FloatField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sponsor} is sponsor for {self.student}"
