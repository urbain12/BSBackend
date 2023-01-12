from rest_framework import serializers

from .models import *

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    user_id = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','FirstName','LastName','MName','FName','Weight','Height','DOB','email','phone','PBirth','remVax','takeVax',]


class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = '__all__'

class VaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccines
        fields = '__all__'
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['user'] is not None:
            data['user'] = UserSerializer(
                User.objects.get(pk=data['user'])).data
        return data


class QueriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queries
        fields = '__all__'