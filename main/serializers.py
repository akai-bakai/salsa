from rest_framework import serializers

from .models import Category, Product, ProductImage, Review, OrderProduct, Order


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
        representation['review'] = ReviewSerializer(instance.review.all(), many=True).data
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

#review
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'review', 'created_at', 'updated_at', 'product')

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['owner_id'] = user_id
        review = Review.objects.create(**validated_data)
        return review

#order
class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    delivery_address = serializers.CharField(required=True)
    order_products = OrderProductSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ('delivery_address', 'order_products')

    def create(self, validated_data):
        order_products = validated_data.pop('order_products')
        order = Order.objects.create(**validated_data)
        for item in order_products:
            product = item['product']
            OrderProduct.objects.create(
                order=order, product=product, price=product.price,
                quantity=item['quantity']
            )
        return order


    def to_representation(self, instance):
        representation = super(OrderSerializer, self).to_representation(instance)
        representation['order_products'] = OrderProductSerializer(
            instance=instance.products.all(), many=True, context=self.context).data
        return representation
