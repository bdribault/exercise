#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(source='profile.birthday', format="%d/%m/%Y")

    class Meta:
        model = User
        fields = ("id", "username", "birthday")


class DetailedUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ("is_superuser", "is_staff")
