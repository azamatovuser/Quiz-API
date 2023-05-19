from rest_framework import serializers
from .models import Account
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'first_name', 'last_name', 'image', 'bio']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=60, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=60, write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError({'success': False, 'message': "Password didn't match, Please try again!"})
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        return Profile.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=60, write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    def get_tokens(self, obj):  # get_{field_name}
        username = obj.get('username')
        tokens = Account.objects.get(username=username).tokens
        return tokens

    class Meta:
        model = Account
        fields = ('username', 'password', 'tokens')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed({
                'message': "Username or Password wrong, Please try again!"
            })
        if not user.is_active:
            raise AuthenticationFailed({
                'message': 'Account disabled'
            })
        return attrs


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'first_name', 'last_name')


class MyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'image', 'first_name', 'last_name', 'created_date')
