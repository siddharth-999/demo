from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, FamilyRelation, RELATION_CHOICE


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
        fields = ("first_name", "last_name", "email", "date_of_birth",
                  "address", "phone_number",)

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
    family = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email",
                  "address", "date_of_birth", "phone_number",
                  "family",)

    def get_family(self, obj):
        return obj.family.name


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class FamilyRelativeDetailSerializer(serializers.ModelSerializer):
    relative = UserBasicSerializer()
    relation_name = serializers.SerializerMethodField()

    class Meta:
        model = FamilyRelation
        fields = ("id", "relative", "relation", "relation_name",)

    def get_relation_name(self, obj):
        return obj.get_relation_display()


class FamilyRelativeCreateSerializer(serializers.ModelSerializer):
    relation = serializers.ChoiceField(allow_null=False, allow_blank=False,
                                       choices=RELATION_CHOICE)

    class Meta:
        model = FamilyRelation
        fields = ("relative", "relation",)

    def validate(self, attrs):
        user = self.context['request'].user
        if not attrs.get('relative'):
            raise ValidationError({"detail": "please enter relative"})
        if FamilyRelation.objects.filter(relative=attrs.get('relative'),
                                         added_by=user).exists():
            raise ValidationError({"detail": "relative is already exists"})
        if attrs.get('relative') == user:
            raise ValidationError({"detail": "please enter valid relative"})
        attrs['added_by'] = user
        return attrs


class FamilyRelativeUpdateSerializer(serializers.ModelSerializer):
    relation = serializers.ChoiceField(allow_null=False,
                                       allow_blank=False,
                                       choices=RELATION_CHOICE)

    class Meta:
        model = FamilyRelation
        fields = ("relative", "relation",)

    def validate(self, attrs):
        user = self.context['request'].user
        if attrs.get('relative') is None:
            raise ValidationError({"detail": "please enter relative"})
        if attrs.get('relative'):
            if attrs.get('relative') == user:
                raise ValidationError({"detail": "please enter valid relative"})
            if attrs.get('relative') != self.instance.relative:
                if FamilyRelation.objects.filter(relative=attrs.get('relative'),
                                                 added_by=user).exists():
                    raise ValidationError({"detail": "relative is already exists"})
        return attrs
