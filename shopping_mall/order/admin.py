from django.contrib import admin
from django.utils.html import format_html
from .models import Order

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_filter = ('status', )
    list_display = ('user', 'product', 'styled_status')
    
    def styled_status(self, obj):
        # '<b>' + obj.status + '</b>'
        # '<b>%s</b>'%(obj.status)
        # '<b>{}</b>'.format(obj.status)
        # f'<b>{obj.status}<b>'
        if obj.status == '환불':
            return format_html(f'<span style="color:red">{obj.status}</span>')
        if obj.status == '결제완료':
            return format_html(f'<span style="color:green">{obj.status}</span>')
        return obj.status
    
    styled_status.short_description = '상태'

admin.site.register(Order, OrderAdmin)