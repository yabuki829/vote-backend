import profile
from urllib import request, response
from rest_framework import generics
from rest_framework import viewsets,views,status
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination
from . import serializers
from .serializers import ChoiceSerializer, ProfileSerializer, VoteSerializer,UserSerializer
from .models import User,Vote,VoteComment,Thread,ThreadComment,Choice,Profile
from rest_framework import permissions
from rest_framework.response import Response 
from rest_framework.parsers import FormParser, MultiPartParser


class IsAdminOrReadOnly(permissions.BasePermission):
    """管理者以外読み取り専用"""

    def has_permission(self, request, view):
        """GET, HEAD, OPTIONS は常に許可"""
        if request.method in permissions.SAFE_METHODS:
            return True

        # 管理者のみすべて許可
        return request.user.is_superuser

class CreateUserView(generics.CreateAPIView):
  serializer_class = UserSerializer
  permission_classes = [AllowAny,]

class ProfileViewSets(viewsets.ModelViewSet):
  queryset = Profile.objects.all()
  serializer_class = ProfileSerializer

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

class VoteViewSet(viewsets.ModelViewSet):
  print("VoteViewSetが呼ばれました")
  queryset = Vote.objects.all()
  serializer_class = VoteSerializer
  
  def perform_create(self, serializer):
    print("VoteViewSet/Createが呼ばれました")
    user = Profile.objects.get(user=self.request.user)
    
    serializer.save(user=user)

class ChoiceViewSets(viewsets.ModelViewSet):
  print("ChoiceViewSetsが呼ばれました")
  queryset = Choice.objects.all()
  serializer_class = ChoiceSerializer
  
  def perform_create(self, serializer):
    print("ChoiceViewSets/Createが呼ばれました")
    serializer.save(user=self.request.user)




# {
#     "id": 3,
#     "user": {
#         "id": 1,
#         "nickName": "user-6です",
#         "user": {
#             "id": 6,
#             "email": "test2@gmail.com"
#         },
#         "createdAt": "2022-09-23",
#         "image": "http://127.0.0.1:8000/media/images/profiles/6function_uuid4_at_0x109d6edd0.jpg"
#     },
#     "questionText": "最高の言語は????",
#     "createdAt": "2022-09-22",
#     "image": null,
#     "isOnlyLoginUser": true,
#     "choices": [
#         {
#             "id": 1,
#             "text": "Python",
#             "votedUserCount": []
#         },
#         {
#             "id": 3,
#             "text": "Javascript",
#             "votedUserCount": [
#                 {
#                     "id": 1,
#                     "nickName": "user-6です",
#                     "user": {
#                         "id": 6,
#                         "email": "test2@gmail.com"
#                     },
#                     "createdAt": "2022-09-23",
#                     "image": "http://127.0.0.1:8000/media/images/profiles/6function_uuid4_at_0x109d6edd0.jpg"
#                 }
#             ]
#         }
#     ]
# }