from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES)

    def create(self, validated_data):
        role = validated_data.pop("role")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )

        user.profile.role = role
        user.profile.save()

        return user
