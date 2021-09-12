from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Q
from django.contrib import admin
from django.utils.html import format_html
from django.db import transaction
from .models import Order

# Register your models here.
def refund(modeladmin, request, queryset):
    with transaction.atomic():
        qs = queryset.filter(~Q(status='환불'))
        
        # LogEntry에서 수정하고자 하는 모델 타입을 알려줌
        ct = ContentType.objects.get_for_model(queryset.model)
        
        for obj in qs:
            obj.product.stock += obj.quantity
            obj.product.save()
            
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ct.pk,
                object_id=obj.pk,
                object_repr='주문 환불',
                action_flag=CHANGE,
                change_message='주문 환불'
            )
        qs.update(status='환불')

refund.short_description = '환불'

class OrderAdmin(admin.ModelAdmin):
    list_filter = ('status', )
    # list_display에 action 함수를 추가
    list_display = ('user', 'product', 'styled_status', 'action')
    change_list_template = 'admin/order_change_list.html'
    change_form_template = 'admin/order_change_form.html'
    
    actions = [
        refund
    ]
    
    # action 함수: 환불 상태가 아닐 때 환불 버튼을 만들고, 그렇지 않을 때 비활성 환불 버튼 만들기
    def action(self, obj):
        if obj.status != '환불':
            return format_html(f'<input type="button" value="환불" onclick="order_refund_submit({obj.id})" class="btn btn-primary btn-sm">')
        else:
            return format_html(f'<input type="button" value="환불" class="btn btn-primary btn-sm disabled">')
        
    action.short_description = '관리'
    
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
    
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': '주문 목록'}
        
        if request.method == 'POST':
            obj_id = request.POST.get('obj_id')
            if obj_id:
                qs = Order.objects.filter(pk=obj_id)
                # LogEntry에서 수정하고자 하는 모델 타입을 알려줌
                ct = ContentType.objects.get_for_model(qs.model)

                for obj in qs:
                    obj.product.stock += obj.quantity
                    obj.product.save()

                    LogEntry.objects.log_action(
                        user_id=request.user.id,
                        content_type_id=ct.pk,
                        object_id=obj.pk,
                        object_repr='주문 환불',
                        action_flag=CHANGE,
                        change_message='주문 환불'
                    )
                qs.update(status='환불')
                
        return super().changelist_view(request, extra_context)
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        order = Order.objects.get(pk=object_id)
        extra_context = {'title': f'{order.user}님의 {order.product} 주문 수정하기'} 
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)
    
    styled_status.short_description = '상태'

admin.site.register(Order, OrderAdmin)