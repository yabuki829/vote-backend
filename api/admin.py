from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from .models import User,Profile,Thread,ThreadComment,Vote,VoteComment,Choice
# Register your models here.
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ()}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
admin.site.register(User, UserAdmin)

admin.site.register(Profile)
admin.site.register(Thread)
admin.site.register(ThreadComment)


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0
 
 
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('questionText', 'createdAt')
admin.site.register(Vote,QuestionAdmin)
admin.site.register(VoteComment)
admin.site.register(Choice)


