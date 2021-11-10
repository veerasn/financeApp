from django.contrib import admin

# Register your models here.
from .models import Organization, Subject, Project


admin.site.register(Organization)
admin.site.register(Subject)
admin.site.register(Project)