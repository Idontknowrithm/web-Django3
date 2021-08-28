from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', ) # ,를 붙여야 문자열 하나가 아닌 튜플로 인식함
    
admin.site.register(User, UserAdmin)