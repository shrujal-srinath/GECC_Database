# In api/admin.py

from django.contrib import admin
from .models import Player, Match, BattingPerformance, BowlingPerformance, PlayerEditRequest

# 🚨 New custom admin action for edit requests
@admin.action(description='Approve selected player edit requests')
def approve_requests(modeladmin, request, queryset):
    for edit_request in queryset:
        if edit_request.status == 'pending':
            try:
                player = edit_request.player
                # Update the player model with the proposed changes
                for field, value in edit_request.proposed_changes.items():
                    setattr(player, field, value)
                player.save()
                
                # Mark the request as approved
                edit_request.status = 'approved'
                edit_request.save()
            except Exception as e:
                modeladmin.message_user(
                    request,
                    f"Failed to approve request for {player.name}: {e}",
                    level='error'
                )
    
    modeladmin.message_user(request, f"{queryset.count()} requests approved successfully.")


# 🚨 New admin class for the PlayerEditRequest model
class PlayerEditRequestAdmin(admin.ModelAdmin):
    list_display = ('player', 'status', 'requested_on')
    list_filter = ('status',)
    actions = [approve_requests]


# Register your models here.
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(BattingPerformance)
admin.site.register(BowlingPerformance)
admin.site.register(PlayerEditRequest, PlayerEditRequestAdmin) # 👈 Register the new model and admin class