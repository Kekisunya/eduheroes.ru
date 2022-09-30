from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminMyUser(admin.ModelAdmin):
    list_display = ('id', 'username', 'date_joined', 'last_login', 'is_admin', 'is_active', 'is_superuser', 'is_staff', )
    list_display_links = ('id', 'username')
    list_editable = ('is_admin', 'is_active', 'is_superuser', 'is_staff',)
    search_fields = ('username', )


admin.site.register(User, AdminMyUser)
