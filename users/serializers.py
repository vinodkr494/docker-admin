from rest_framework import serializers
from .models import User,Permission,Role

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class PermissionRelatedField(serializers.StringRelatedField):
    def to_representation(self,value):
        #getting the role
        return PermissionSerializer(value).data

    def to_internal_value(self,data):
        #storing the role
        return data

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionRelatedField(many=True)
    class Meta:
        model = Role
        fields = '__all__'

    def create(self,validate_data):
        permissions = validate_data.pop('permissions',None)
        instance = self.Meta.model(**validate_data)
        instance.save()
        instance.permissions.add(*permissions)
        instance.save()
        return instance

class RoleRelatedField(serializers.RelatedField):
    def to_representation(self,instance):
        return RoleSerializer(instance).data

    def to_internal_value(self,data):
        return self.queryset.get(pk=data)

class UserSerializer(serializers.ModelSerializer):
    role = RoleRelatedField(many=False,queryset=Role.objects.all())
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','password','role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self,validate_data):
        password = validate_data.pop('password',None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self,instance,validate_data):
        password = validate_data.pop('password',None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance