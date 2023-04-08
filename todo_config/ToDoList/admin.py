from django.contrib import admin
from .models import UserToken, Task


class UserTokenAdmin(admin.ModelAdmin):
    model = UserToken 

    list_display = ('user', 'token', 'expiry_date', )
    search_fields = ('user__username__icontains', )
    
class TaskAdmin(admin.ModelAdmin):
    model = Task

    list_display = ('user', 'title_slicer', 'created_at', 'updated_at', 'id', )
    list_filter = ('created_at', 'updated_at', )
    search_fields = ('user__username__icontains', 'title', )

    def title_slicer(self, obj):
        title = str(obj.title)
        if len(title) > 15:
            return title[:15] + '.....'
        return title

    title_slicer.short_description = 'Title'



admin.site.register(Task, TaskAdmin)
admin.site.register(UserToken, UserTokenAdmin)