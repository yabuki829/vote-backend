
from rest_framework import generics
from rest_framework import viewsets,views,status
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination
from . import serializers
from .serializers import ChoiceSerializer, ProfileSerializer, VoteSerializer,UserSerializer,QuestionResultPageSerializer,ChoiceSerializerWithVotes
from .models import User,Vote,VoteComment,Thread,ThreadComment,Choice,Profile
from rest_framework import permissions
from rest_framework.response import Response 
from rest_framework.decorators import action
from urllib.request import Request
from django.http import HttpResponse


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
  serializer_class = QuestionResultPageSerializer

  
class ChoiceViewSets(viewsets.ModelViewSet):
  print("ChoiceViewSetsが呼ばれました")
  queryset = Choice.objects.all()
  serializer_class = ChoiceSerializerWithVotes

