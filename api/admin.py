from django.contrib import admin
from .models import Player, Match, BattingPerformance, BowlingPerformance

# Register your models here.
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(BattingPerformance)
admin.site.register(BowlingPerformance)
