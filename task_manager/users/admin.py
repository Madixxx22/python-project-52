from django.contrib import admin

from task_manager.users.models import CustomUser

admin.site.register(CustomUser)
# Register your models here.
# @admin.register(CustomUser)
# class CustomUserAdmins(UserAdmin):
#    model = CustomUser
#    form = CustomUserChangeForm
#    add_form = CustomUserCreationForm

#    add_fieldsets = (
#        *UserAdmin.add_fieldsets, (
#            'Custom fields',
#            {
#               'fields': (
#                    'first_name',
#                    'last_name',
#                )
#            }
#        )
#    )

#    fieldsets = (
#        *UserAdmin.add_fieldsets, (
#            'Custom fields',
#            {
#                'fields': (
#                    'first_name',
#                    'last_name',
#                )
#           }
#        )
#    )
