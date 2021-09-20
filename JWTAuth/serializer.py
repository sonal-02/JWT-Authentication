from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User
from datetime import date
from .models import User


def age_restriction(dob):
    """
    This function is for check restriction, if manager enter the date of birth and him/her age
    less than 18 then he/she can't signup.
    :param dob: 2018-02-01
    :return: validation error
    """
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if not (18 < age):
        raise serializers.ValidationError("You age should be greater than 18 to eligible for the work")
    return dob


def is_manager_restriction(manager):
    """
    This  function is used to check role is is_manager or not. If role is not is_manager then can't signup.
    Only manager can signup and employee can created only by manager.
    :param manager: False
    :return: validation error
    """
    if manager is False:
        raise serializers.ValidationError("Employee can't signup")
    return manager


class UserSerializer(serializers.ModelSerializer):
    """
    This serializer is used for manager signup only.
    """
    is_manager = serializers.BooleanField(required=True, validators=[is_manager_restriction])
    dob = serializers.DateField(validators=[age_restriction])
    address = serializers.CharField(required=False)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'firstname', 'lastname', 'dob', 'company', 'is_manager', 'address']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_manager': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Used to create encrypted password
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    """
    Login serializer for manager only.
    """

    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CURDSerializer(serializers.ModelSerializer):
    """
    This serializer is used to perform CURD operation for employee. Only manager can do this operation.
    """
    dob = serializers.DateField(validators=[age_restriction])
    address = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    mobile = serializers.CharField(required=False)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'firstname', 'lastname', 'dob', 'company', 'city', 'mobile', 'address']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """
        Used to create encrypted password
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        Used to create encrypted password while updating employee password.
        """
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
