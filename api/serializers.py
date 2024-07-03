from rest_framework import serializers

from api.models import User, Category


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
