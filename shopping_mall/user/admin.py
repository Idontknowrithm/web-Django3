from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', ) # ,를 붙여야 문자열 하나가 아닌 튜플로 인식함
    
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': '사용자 목록'}
        return super().changelist_view(request, extra_context)
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        user = User.objects.get(pk=object_id)
        extra_context = {'title': f'{user.email} 수정하기'}
        return super().changeform_view(request, object_id, form_url, extra_context)
    
admin.site.register(User, UserAdmin)
admin.site.site_header = 'Django backoffice1'
admin.site.index_title = 'Django backoffice2'
admin.site.site_title = 'Django backoffice3'