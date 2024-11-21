from rest_framework import serializers
from .models import UserRegistration, Partnership, Resource, Event, Post

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegistration
        fields = ['username', 'password', 'email', 'user_type', 'bio']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Use create instead of create_user
        user = UserRegistration.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            user_type=validated_data['user_type'],
            bio=validated_data.get('bio', '')
        )
        # Manually set the password and save it using Django's hashing
        user.password = validated_data['password']
        user.save()
        return user

class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Post
        fields = [
           'id' ,'text', 'username', 'created_at', 'sus', 'sdg_names', 'sdg_descriptions', 
            'target_names', 'target_descriptions', 'sustainability_dimensions'
        ]


class PartnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partnership
        fields = ['user', 'partner', 'status', 'created_at']

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'uploaded_by', 'file', 'created_at']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'created_by']


class UserProfileSerializer:
    pass