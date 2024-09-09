from .models import FriendRequest, Profile
from django.contrib.auth.models import User
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("username", "email", "id")

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = "__all__"

class FriendListSerializer(serializers.ModelSerializer):

    receiver = ProfileSerializer()

    class Meta:
        model = FriendRequest
        fields = ("id", "receiver", "timestamp")

class ReceivedRequestSerializer(serializers.ModelSerializer):

    sender = ProfileSerializer()

    class Meta:
        model = FriendRequest
        fields = ("id", "sender", "timestamp")