from django.contrib import admin
from .models import UnApprovedUsersModel,NotificationModel
from usersection.models import SignUpModel


# Register your models here.
admin.site.register(UnApprovedUsersModel)
admin.site.register(SignUpModel)
admin.site.register(NotificationModel)
