from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(School)
admin.site.register(Test)
admin.site.register(Student)
admin.site.register(Marks)