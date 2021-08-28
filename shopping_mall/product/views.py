from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from rest_framework import generics, mixins


from user.decorators import admin_required
from .models import Product
from .forms import RegisterForm
from .serializers import ProductSerializer
from order.forms import RegisterForm as OrderForm

# Create your views here.

class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    # 데이터에 대한 검증
    serializer_class = ProductSerializer
    
    # 어떤 데이터를 들고 올 건지
    def get_queryset(self):
        return Product.objects.all().order_by('id')
    
    def get(self, request, *args, **kwargs):
        # mixin에 들어있는 list함수 사용
        return self.list(request, *args, **kwargs)

class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    # 데이터에 대한 검증
    serializer_class = ProductSerializer
    
    # 어떤 데이터를 들고 올 건지
    def get_queryset(self):
        return Product.objects.all().order_by('id')
    
    def get(self, request, *args, **kwargs):
        # mixin에 들어있는 팝업용 retrieve함수 사용
        return self.retrieve(request, *args, **kwargs)
    
class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    # context_object_name = 'product_list'

@method_decorator(admin_required, name='dispatch')
class ProductCreate(FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'
    
    def form_valid(self, form):
        product = Product(
            name=form.data.get('name'),
            price=form.data.get('price'),
            description=form.data.get('description'),
            stock=form.data.get('stock')
        )
        product.save()
        # form_valid는 오버라이딩 됐기 때문에 부모의 함수를 호출함
        return super().form_valid(form)
    
class ProductDetail(DetailView):
    template_name = 'product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'
    
    # 원하는 데이터를 넣을 수 있는 함수 제공
    def get_context_data(self, **kwargs):
        # detailview가 자동으로 전달해주는 데이터를 먼저 만들어주고 나서
        context = super().get_context_data(**kwargs)
        # 내가 원하는 데이터를 추가
        context['form'] = OrderForm(self.request)
        return context