from rest_framework import serializers

from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Category


class ProductSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        fields = ('__all__')
        model = Product


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.email
        representation['category'] = CategorySerializer(instance.category).data
        representation['images'] = ProductImageSerializer(instance.images.all(),
                                                       many=True, context=self.context).data
        return representation

#need to change this permission, so only admin can make changes in the post
    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['owner_id'] = user_id
        post = Product.objects.create(**validated_data)
        return post


class ProductImageSerializer(serializers.ModelSerializer):   # try to find other way
    class Meta:
        fields = ('__all__')
        model = ProductImage

        def _get_image_url(self, obj):
            if obj.image:
                url = obj.image.url
                request = self.context.get('request')
                if request is not None:
                    url = request.build_absolute_uri(url)
            else:
                url = ''
            return url

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['image'] = self._get_image_url(instance)
            return representation