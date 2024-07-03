from rest_framework import serializers

from api.models import User, Category, Storage, Ingredient, Product, HomePageSlider, Order, OrderItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'password', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Handle password
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
        return instance

    def update(self, instance, validated_data):
        # Handle password
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class OTPLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)


class OTPVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    otp = serializers.CharField(max_length=6)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ['id', 'name', 'amount']


class IngredientSerializer(serializers.ModelSerializer):
    storage_id = serializers.PrimaryKeyRelatedField(queryset=Storage.objects.all(), source='storage')

    class Meta:
        model = Ingredient
        fields = ['storage_id', 'quantity']


class ProductSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image', 'price', 'category', 'ingredients']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        product = super().create(validated_data)

        for ingredient_data in ingredients_data:
            Ingredient.objects.create(product=product, **ingredient_data)

        return product

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        product = super().update(instance, validated_data)

        for ingredient_data in ingredients_data:
            ingredient, _ = Ingredient.objects.get_or_create(product=product)
            ingredient.quantity = ingredient_data.get('quantity')
            ingredient.storage = ingredient_data.get('storage')
            ingredient.save()

        return product


class HomePageSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageSlider
        fields = ['image']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class CategoryProductsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ['products']


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")

        if not product.has_enough_stock():
            raise serializers.ValidationError("Out of stock.")
        return value

    def create(self, validated_data):
        order, _ = Order.objects.get_or_create(user=self.context['request'].user, is_paid=False)
        order_item, created = OrderItem.objects.get_or_create(
            order=order, product_id=validated_data.get('product_id')
        )
        if not created:
            order_item.quantity += 1
            order_item.save()
        return order_item


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.IntegerField(source='product.price', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_name', 'product_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Order
        fields = ['items', 'amount', 'created_at', 'is_takeaway']


class PayOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['is_takeaway']


class ProductSalePerDaySerializer(serializers.Serializer):
    day = serializers.DateTimeField(format="%Y-%m-%d")
    sale_count = serializers.IntegerField()
