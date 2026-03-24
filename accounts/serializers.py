from django.contrib.auth.models import User
from accounts.models import Profile
from rest_framework import serializers
from .models import Profile, Task
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username','email','password')
        # extra_kwargs = {'password2': {'write_only': True}}

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value
   
    def create(self, validated_data):
        #validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Profile.objects.create(user=user)
        return user

###################################################################################################################################   
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
    
################################################################################

# class UpdateProfileSerializer(serializers.ModelSerializer):

#     username = serializers.CharField(source='user.username')
#     email = serializers.EmailField(source='user.email')

#     class Meta:
#         model = Profile
#         fields = ('username', 'email','address', 'phone', 'bio', 'age')

        
#     def validate_email(self,value):
#         try:
#             validate_email(value)
#         except ValidationError:
#             raise serializers.ValidationError("Enter a valid email address.")
#         if User.objects.filter(email=value).exclude(pk=self.instance.user.pk).exists():
            
#         # user = self.instance
#         # if User.object.exclude(pk=user.pk).filter(email=value).exists():
#             raise serializers.ValidationError("Email already registered")
#         return value

class UpdateProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ('username', 'email',) #'address', 'phone', 'bio', 'age')

    def update(self, instance, validated_data):
        # instance.username = validated_data.get('username', instance.username)
        # instance.email = validated_data.get('email', instance.email)
       
        user = instance.user

        # Update User fields
        if 'username' in validated_data:
        #if"username" in user_data:
            user.username = validated_data['username']

        if 'email' in validated_data:
            user.email = validated_data['email']

        user.save()
        return instance
        # user.save()

        # Update Profile fields
        #return super().update(instance, validated_data)

##################################################################################################################################################################

    
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email')
####################################################################################################################################################

# from django.contrib.auth.models import User
# from accounts.models import Profile
# from rest_framework import serializers

# class RegisterSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password']
#         )
#         Profile.objects.create(user=user)
#         return user


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email')
