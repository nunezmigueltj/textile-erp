from django.contrib import admin
from .models import PullRequest, PullRequestLine

# Register your models here.
admin.site.register(PullRequest)
admin.site.register(PullRequestLine)