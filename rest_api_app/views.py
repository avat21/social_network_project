from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.utils.timezone import now
from datetime import timedelta

from .models import FriendRequest, Profile
from .serializer import *

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination

import re

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        try:

            data = request.data
            email = data.get('email')

            pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

            if re.match(pattern, email):

                if User.objects.filter(username=email).exists() or Profile.objects.filter(email=email).exists():
                    return Response({'success':False, 'response': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)
                
                user = User.objects.create(username=email)

                username, other = email.split("@")

                profile = Profile.objects.create(email=email, username=username, auth_user=user)

                return Response({"success":True, "response": "user created successfully", "user":profile.id}, status=status.HTTP_201_CREATED)
            
            else:
                return Response({"success":False, "response": "email validation failed"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:

            return Response({"success":False, "response": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, user_id):

        try:

            username = request.data.get("username")
            password = request.data.get("password")

            if not Profile.objects.filter(id=user_id).exists():
                return Response({"success":False, "response":"User not found"}, status=status.HTTP_400_BAD_REQUEST)

            profile = Profile.objects.get(id=user_id)

            if profile.username != username:
                if Profile.objects.filter(username=username).exists():
                    return Response({"success":False, "response":"username already found"}, status=status.HTTP_400_BAD_REQUEST)

            profile.username = username
            profile.save()

            profile.auth_user.set_password(password)
            profile.auth_user.save()

            return Response({"success": True, "response": "user details updated successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:

            return Response({"success":False, "response": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        if Profile.objects.filter(email=email).exists() and User.objects.filter(username=email):

            user = authenticate(username=email, password=password)

            if user is not None:

                # login(request, user)

                token = RefreshToken.for_user(user)

                return Response({"success":True, "response": "user logged in successfully", "access": str(token.access_token), "refresh": str(token)}, status=status.HTTP_200_OK)

            else:

                return Response({"success":False, "response": "authentication failed"}, status=status.HTTP_400_BAD_REQUEST)

        else:

            return Response({"success":False, "response":"user not found"}, status=status.HTTP_400_BAD_REQUEST)        

class SendFriendRequestView(APIView):

    def post(self, request):
        
        sender = request.data.get('sender')
        receiver = request.data.get('receiver')

        if Profile.objects.filter(id=sender).exists() and Profile.objects.filter(id=receiver).exists():

            if not FriendRequest.objects.filter(sender__id=sender).filter(receiver__id=receiver).exists():

                time_check = now() - timedelta(minutes=1)

                recent_requests = FriendRequest.objects.filter(sender__id=sender).filter(timestamp__gte=time_check)

                print(recent_requests)

                if len(recent_requests) <= 2:

                    FriendRequest.objects.create(
                        sender=Profile.objects.get(id=sender),
                        receiver=Profile.objects.get(id=receiver)
                    )

                    return Response({"success":True, "response": "user request created successfully"}, status=status.HTTP_201_CREATED)

                else:

                    return Response({"success":False, "response":"Request limit exceeded"}, status=status.HTTP_400_BAD_REQUEST)

            else:

                return Response({"success":False, "response":"already request found"}, status=status.HTTP_400_BAD_REQUEST)
        
        else:

            return Response({"success":False, "response":"sender / receiver not found"}, status=status.HTTP_400_BAD_REQUEST)
    
class ModifyRequestStatusView(APIView):
    def post(self, request):

        sender = request.data.get('sender')
        receiver = request.data.get('receiver')
        status = request.data.get('status')

        query = FriendRequest.objects.filter(sender__id=sender).filter(receiver__id=receiver).first()

        if query is not None:

            query.status = status
            query.save()

            serialized_data = FriendRequestSerializer(query).data

            return Response(serialized_data)

        else:

            return Response({"success":False, "response":"request is not found"}, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    def get(self, request):

        search = request.GET.get('search', None)

        if search is not None:

            profile = Profile.objects.filter(Q(username__icontains=search) | Q(email__icontains=search))

        else:

            profile = Profile.objects.all()

        paginator = PageNumberPagination()

        paginator.page_size = 10

        result_page = paginator.paginate_queryset(profile, request)

        serialized_data = ProfileSerializer(result_page, many=True)

        return paginator.get_paginated_response(serialized_data.data)

class UserFriendList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):

        friend_list = FriendRequest.objects.filter(sender__id=user_id).filter(status="accepted")

        serialized_data = FriendListSerializer(friend_list, many=True).data

        return Response(serialized_data, status=status.HTTP_200_OK)

class UserPendingRequestView(APIView):
    def get(self, request, user_id):

        pending_request = FriendRequest.objects.filter(receiver__id=user_id).filter(status="pending")

        serialized_data = ReceivedRequestSerializer(pending_request, many=True).data

        return Response(serialized_data, status=status.HTTP_200_OK)