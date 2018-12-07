from django.contrib import admin

from .models import Competition, Match, Participant

admin.site.register(Competition)
admin.site.register(Match)
admin.site.register(Participant)
