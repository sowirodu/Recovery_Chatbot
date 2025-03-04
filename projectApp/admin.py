from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Question,TreatmentCenter,Insurance

admin.site.register(Question)

admin.site.register(TreatmentCenter)

admin.site.register(Insurance)