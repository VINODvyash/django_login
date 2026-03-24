from django.contrib.auth.models import User
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UpdateProfileSerializer
from .models import Task
from django.contrib.auth import authenticate
import random
from django.utils import timezone
from .serializers import TaskSerializer
from .permissions import IsAdminUserCustom
from rest_framework.test import APIClient
from rest_framework.views import APIView
# from .views import TaskViewSet

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUserCustom])
def admin_dashboard(request):
     return Response({"message": "Welcome, Admin",
                      "user": request.user.username,
                      "role": " Admin Acess Granted"
                      })


# --------------------
# Health Check API (Working)
# --------------------
@api_view(['GET'])
def health(request):
    return Response({"status": "OK"})


#-----------------------------------
#login API (JWT) (Working)
#-----------------------------------

@api_view(['POST'])
# @permission_classes([AllowAny]) #Allow any user (authenticated or not) to access this view


def login_view(request):
    
        email = request.data.get('email')
        username =request.data.get('username')
        password = request.data.get('password')
       

        if not username or not password:
            return Response(
                {"error" : "username and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        #Authenticate User
        user = authenticate(username=username, password=password)  

        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        
        #JWT token
        refresh = RefreshToken.for_user(user)

        return Response(
           {
            "message": "Login successful",
            "user": UserSerializer(user).data,
                        
            #serSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
            },
            status=status.HTTP_200_OK
        )

   
#------------------------------------
#Protected PROFILE API (JWT required) (Running)
#------------------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # authenticated users can access this view
def profile(request):
    profile = request.user.profile

    serializer = UserSerializer(request.user)
    profile_serializer = UpdateProfileSerializer(profile)

    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "EMAIL": request.user.email,
        "message": "You accessed a protected API"
    })

from .serializers import RegisterSerializer,UserSerializer


#---------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUserCustom])
def admin_only_view(request):
    return Response({"message": "Admin access granted"})
#---------------------------------------------


#------------------------------------
# Register API (Working)
#------------------------------------


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        
        user = serializer.save()

        # Profile.objects.create(user=isinstance)

        #Genrate JWT token
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User registered successfully",
                "user": {
                 "id": user.id,
                  "username": user.username,
                  "email": user.email,
                  "Password": user.password
                  
            },

            "refresh":str(refresh),
            "access": str(refresh.access_token),
            
            
            },

            status=status.HTTP_201_CREATED
       )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):

    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_205_RESET_CONTENT
        )

    except Exception as e:
        return Response(
            {"error": "Invalid token or token already blacklisted"},
       
            status=status.HTTP_400_BAD_REQUEST
        )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_api(request):
    return Response({"message": "You have accessed a protected API", "user": request.user.username})

##################################################################################################################

@api_view(['PUT','PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = request.data

    # Update User fields
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        if len(password) < 6:
            return Response({"password": ["Password must be at least 6 characters."]}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
    user.save()

    # Update Profile fields
    profile = user.profile
    serializer = UpdateProfileSerializer(profile, data=data, partial=True)
    if serializer.is_valid():
         serializer.save()

         return Response({
             
                "username": user.username,
            "email": user.email,
            "message": "Profile updated successfully."
        }, status=status.HTTP_200_OK)

    # else:
    #     print("❌ Serializer errors:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Change password API

@api_view(['post'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user= request.user

    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not user.check_password(old_password):
        return Response({"error": "old password is incorrect"},status=400)
    
    if len(new_password) <6:
        return Response({"error": "password must be at least 6 characters long"}, status=400)
    
    user.set_password(new_password)
    user.save()

    return Response({"message": "password changed successfully"}, status=200)


#Forgot password API

@api_view(['post'])
def forgot_password(request):
    email = request.data.get('email')

    if not email:
        return Response({"error": "Email required"}, status=400)
    
    try:
        user = User.objects.get(email=email)

        # Here, you would typically send a password reset email with a tokenized link
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    
    #Genrate OTP
    otp = random.randint(100000, 999999)

    # if user.profile.reset_otp != int(otp):
    #     return Response ({"error": "Invalid OTP"}, status=400)
    
    user.profile.reset_otp = otp
    user.profile.otp_created_at = timezone.now()
    user.profile.save()

    #simulate email sending
    print("OTP:", otp)

    return Response({"message": "OTP sent to your email"}, status=200)


#Reset Password

@api_view(['POST'])
def reset_password(request):

    email = request.data.get('email')
    otp = request.data.get('otp')
    new_password = request.data.get('new_password')

    if not email or not otp or not new_password:
        return Response({"error": "Email, OTP, and new password are requiresd"},
                         status=400)
    
    try: 
        user = User.objects.get(email=email)
        profile = user.profile
    except User.DoesNotExist:
        return Response({"error": "invalid OTP"}, status=400)
    
    

    #otp validation 

    # if profile.otp != otp:
    if profile.reset_otp != str(otp):
        return Response({"error": "Invalid OTP"}, status=400)
    
    #OTP expiry check

    if timezone.now() > profile.otp_created_at + timedelta(minutes=5):
        return Response({"error": "OTP expired"}, status=400)
    
    #Reset password

    user.set_password(new_password)
    user.save()

    #clear OTP
    
    profile.reset_otp = None
    profile.otp_created_at = None
    profile.save()

    return Response(
        {"message": "Password reset successful"}, 
        status=200
    )


import pytest
from rest_framework.test import APIClient

# @pytest.mark.django_db
def test_login_success():
    client = APIClient()

    # 👇 CREATE USER IN TEST DATABASE
    User.objects.create_user(
        username="priyaannu",
        # email="priya@test.com",
        password="vinod@iloveyouu"
    )

    payload = {
        "username": "priyaannu",
        "password": "vinod@iloveyouu"
    }

    response = client.post("/api/login/", payload, format="json")

    print(response.data)

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


    #Logged-in User API


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user = request.user

        data = {
            "id" : user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            # "is_active": user.is_active,
            # "is_staff": user.is_staff
        }

        return Response({
            "status" : True,
            "message": "user profile retrived succesfully",
            "data": data
        }, status = status.HTTP_200_OK)
    
class TaskViewSet(viewsets.ModelViewSet):
    Serializer_calss = TaskSerializer
    permission_classes = [IsAdminUserCustom]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_creat(self, serializer):
        serializer.save(user=self.request.user)


    # def get(self, request):
    #     tasks = Task.objects.filter(user=request.user)
    #     serializer = TaskSerializer(tasks, many=True)
    #     return Response(serializer.data)
        
    # def post(self, request):
    #     serializer = TaskSerializer(data=request.data)
    #     if serializer.is_valid():
    #             # serializer.save(serializer.data, status=status.HTTP_201_CREATED)
    #             # return Response(serializer.data, staus=status.HTTP_400_BAD_REQUEST)
    #         serializer.save(user=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






    # otp = random.randint(100000, 999999)

    # user.set_password(new_password)
    # user.save()

    # #Clear otp
    # user.profile.reset_otp = None
    # User.profile.save()
    # print("OTP:", otp)

    # return Response(
    #     {"message": "Password reset successfull"}, status=200)

    # user.profile.otp_crated = timezone.now()

    # if timezone.now() > user.profile.otp_created_at + timedelta(minutes =5):
    #     return Response({"error": "OTP expired"}, status=400)
    

