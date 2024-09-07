from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Ranks


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('__str__', 'position', 'company', 'phone', 'is_staff', 'is_active', 'is_superuser',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        ('Учетная запись', {'fields': ('email', 'password',)}),
        ('Персональные данные', {'fields': ('last_name', 'first_name', 'middle_name', 'phone',)}),
        ('Место работы', {'fields': ('company', 'position', 'rank',)}),
        ('Согласие на обработку персональных данных', {'fields': ('agreement',)}),
        ('Активность', {'fields': ('date_joined', 'last_login',)}),
        ('Группы', {'fields': ('groups',)}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('last_name', 'first_name', 'middle_name', 'email', 'company',)
    ordering = ('last_name', 'first_name', 'middle_name', 'email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Ranks)

