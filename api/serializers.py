from rest_framework import serializers

from api.models import User, Category, Storage, Ingredient, Product, HomePageSlider


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
            Ingredient.objects.create(product=product, **ingredient_data)

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
