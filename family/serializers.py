from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class LoginAuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, allow_blank=False,
                                     allow_null=False, max_length=50)
    username = serializers.EmailField(max_length=225, required=True,
                                      allow_blank=False, allow_null=False)

    class Meta:
        model = User
        fields = ('username', 'password')


class UserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(allow_null=False, allow_blank=False,
                                       max_length=15)
    last_name = serializers.CharField(allow_null=False, allow_blank=False,
                                      max_length=15)
    email = serializers.EmailField(max_length=100, allow_null=False,
                                   allow_blank=False)
    date_of_birth = serializers.DateField(allow_null=False)
    phone_number = serializers.IntegerField(allow_null=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",
                  "address", "date_of_birth", "phone_number",)

    def validate(self, attrs):
        username = attrs.get("email")
        if username and username != self.instance.username:
            if User.objects.filter(
                    username=username).exclude(id=self.instance.id
                                               ).exists():
                raise ValidationError({"detail": "username is taken"})
            attrs["username"] = username
        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "description", "email", "username",
                  "address", "date_of_birth")
