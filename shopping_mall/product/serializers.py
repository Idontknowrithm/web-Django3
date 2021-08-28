from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        # model은 Product를 사용
        model = Product
        # 모든 필드를 가져옴
        fields = '__all__'