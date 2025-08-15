from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # p1 = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)
    p2 = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)

    class Meta:
        model = User
        fields = 'email', 'password', 'p2'

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('p2')

        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпали')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 100, required = True)


class RestorePasswordSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(min_length=8, required=True)
    password2 = serializers.CharField(min_length=8, required=True)

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if password2 != attrs['password']:
            raise serializers.ValidationError('Не совпадает!')
        try:
            user = User.objects.get(activation_code=attrs['code'])
        except User.DoesNotExist:
            serializers.ValidationError('Нет такого пользователя!')
        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        user = data['user']
        user.set_password(data['password'])
        user.activation_code = ''
        user.save()
        return user