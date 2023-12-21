from django.contrib import admin
from .models import Job, Response
class PostAdmin(admin.ModelAdmin):
    search_fields = ('name')

admin.site.register(Job)
admin.site.register(Response)