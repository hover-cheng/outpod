from django.contrib import admin
from saltapi.models import GroupList, ServerList, CommandList, OperationLog, ProjectList, \
    AppName, MvnType, MvnOrder, UserProfile

# Register your models here.
admin.site.register(GroupList)
admin.site.register(ServerList)
admin.site.register(CommandList)
admin.site.register(OperationLog)
admin.site.register(ProjectList)
admin.site.register(AppName)
admin.site.register(MvnType)
admin.site.register(MvnOrder)
admin.site.register(UserProfile)
