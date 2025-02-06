from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    def validate_password(self, value: str) -> str:
        return make_password(value)


class ModifiedObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if user.is_staff:
            token['group'] = 'admin'
        else:
            token['group'] = 'user'
            token['role'] = user.account_type

        return token


class ModifiedTokenObtainPairView(TokenObtainPairView):
    serializer_class = ModifiedObtainPairSerializer
