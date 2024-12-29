from django.contrib.auth.models import User
from django.db import models

ROLE_CHOICES = (
    ('collector', 'Collector'),
    ('school', 'School'),
    ('other', 'Other'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class School(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Test(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    date = models.DateField()
    question_file = models.FileField(upload_to='test_files/', null=True, blank=True)
    answer_file = models.FileField(upload_to='test_files/', null=True, blank=True)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    roll_number = models.CharField(max_length=50)

from django.db import models

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    marks = models.IntegerField()
    
    def __str__(self):
        return f"{self.student.name} - {self.test.name}: {self.marks}"


