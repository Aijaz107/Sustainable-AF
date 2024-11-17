from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from datetime import date
from seesus import SeeSus
import requests
from transformers import pipeline

from .models import UserRegistration, Post
from .serializers import UserRegistrationSerializer, UserProfileSerializer, PostSerializer
from .models import Partnership
from .serializers import PartnershipSerializer
from .models import Resource
from .serializers import ResourceSerializer
from .models import Event
from .serializers import EventSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import json

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def analyze_post(request):
    try:
        # Parse the JSON payload
        data = json.loads(request.body)

        # Retrieve the 'post_text' field
        post_text = data.get('post_text', '')

        # Validate that 'post_text' is provided
        if not post_text:
            return Response(
                {"error": "No post_text provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = SeeSus(post_text)
        response = {"result": result.sus}

        return Response(response, status=status.HTTP_200_OK)

    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON payload"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def title_generator(request):
        
        content = request.data.get('content')
        
        API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
        headers = {"Authorization": "Bearer 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"}


        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        # Check if content is provided
        if not content:
            return Response({"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Make the POST request to the external API
        try:
            # summarizer = pipeline("summarization", model="path-to-model")
            # summary = summarizer(content)[0]["summary_text"]
            output = query({"inputs":content, "parameters":{"min_length":20,"max_length":50}})
            print("respone",query({"inputs":content, "parameters":{"min_length":20,"max_length":50}}))
            # Parse the response and extract the desired result
            return Response(output.json(), status=status.HTTP_201_CREATED )
        except requests.RequestException as e:
            return Response({"error": f"Request failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# User Registration
@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    serializer = UserRegistrationSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Check if username and password are provided
    if not username or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Manually get the user by username
        user = UserRegistration.objects.get(username=username)
    except UserRegistration.DoesNotExist:
        return Response({"error": "Invalid username or password 1"}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if the password matches
    if password != user.password:
        return Response({"error": "Invalid username or password 2"}, status=status.HTTP_401_UNAUTHORIZED)

    # Success: Login is valid
    return Response({
        "message": "Login successful",
        "username": user.username,
        "email": user.email,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def post_list(request):
    """Get all posts."""
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_post(request):
    """Create a new post without requiring authentication, using the provided username."""
    data = request.data.copy()  # Copy request data to modify it

    # Check if the username exists in the data
    username = data.get('username')
    if not username:
        return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Find the user by username
        user = UserRegistration.objects.get(username=username)
    except UserRegistration.DoesNotExist:
        return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    # Use the found user ID to populate the data for validation
    data['user'] = user.id

    serializer = PostSerializer(data=data)

    if serializer.is_valid():

        # post_text = serializer.validated_data['text']
        # check_sustainability(post_text)

        # Save the new post using the serializer
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # If the data is invalid, return the errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_post(request, post_id):
    """Edit an existing post by its ID."""
    # Find the post to be updated or return 404 if not found
    post = get_object_or_404(Post, id=post_id)

    # Extract the username from the payload
    username = request.data.get('username')
    if not username:
        return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the username matches the post's owner
    if post.user.username != username:
        return Response({"error": "Permission denied. You can only edit your own posts."}, status=status.HTTP_403_FORBIDDEN)

    # Use serializer to update the post data
    serializer = PostSerializer(post, data=request.data, partial=True)  # Allow partial updates
    if serializer.is_valid():
        serializer.save()  # Save the changes to the post
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Return errors if data is invalid
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Profile View
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserProfileSerializer()
        print(serializer)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Partnership Matching
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def partnership_match(request):
    user = request.user
    potential_partners = UserRegistration.objects.exclude(id=user.id).filter(user_type=user.user_type)
    matches = Partnership.objects.filter(user=user, status="Pending")
    if not matches and potential_partners.exists():
        partner = potential_partners.first()  # Dummy match with the first available partner
        partnership = Partnership(user=user, partner=partner, status="Pending")
        partnership.save()
        serializer = PartnershipSerializer(partnership)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"message": "No match found"}, status=status.HTTP_404_NOT_FOUND)

# Partnership Status
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def partnership_status(request, pk):
    partnership = get_object_or_404(Partnership, id=pk, user=request.user)
    serializer = PartnershipSerializer(partnership)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Resource Upload
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def resource_upload(request):
    serializer = ResourceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(uploaded_by=request.user)
        return Response({"message": "Resource uploaded successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View All Resources
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resource_list(request):
    resources = Resource.objects.all()
    serializer = ResourceSerializer(resources, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# View Resources by Category
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resource_by_category(request, category):
    resources = Resource.objects.filter(category=category)
    serializer = ResourceSerializer(resources, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Event Creation
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def event_create(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response({"message": "Event created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View Upcoming Events
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def upcoming_events(request):
    events = Event.objects.filter(date__gte=date.today()).order_by('date')
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Event Details View
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_detail(request, pk):
    event = get_object_or_404(Event, id=pk)
    serializer = EventSerializer(event)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Predictive Analytics (Placeholder)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def predictive_analytics(request):
    predictions = {
        "partnership_success": 85,  # Placeholder prediction score
        "event_impact": 90         # Placeholder impact score
    }
    return Response(predictions, status=status.HTTP_200_OK)
