
import uuid
from rest_framework import generics
from rest_framework import viewsets,views,status
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination
from . import serializers
from .serializers import ChoiceSerializer, ProfileSerializer, QuestionDetailPageSerializer, VoteSerializer,UserSerializer,QuestionResultPageSerializer,ChoiceSerializerWithVotes
from .models import User,Vote,VoteComment,Thread,ThreadComment,Choice,Profile
from rest_framework import permissions
from rest_framework.response import Response 
from rest_framework.decorators import action
from urllib.request import Request
from django.http import HttpResponse


class CreateUserView(generics.CreateAPIView):
  serializer_class = UserSerializer
  permission_classes = [AllowAny,]

  def perform_create(self, serializer):
    return super().perform_create(serializer)

class ProfileViewSets(viewsets.ModelViewSet):
  queryset = Profile.objects.all()
  serializer_class = ProfileSerializer

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)


  

class VoteAPIView(views.APIView):
  

  def get(self,request):
    vote = Vote.objects.filter()
    serializer = QuestionResultPageSerializer(vote, many=True)
  
    return Response(serializer.data,status=status.HTTP_201_CREATED)
  
  def post(self,request):
    request_data = request.data
    print(request_data)
    serializer = QuestionDetailPageSerializer(data=request_data)
    
    choices = request_data["choices"]
    if serializer.is_valid():
      profile = Profile.objects.get(user=self.request.user) 
      vote_id = str(uuid.uuid4())
      serializer.save(user=profile,id=vote_id)
      print(1111111111111111111)
      vote_instance = Vote.objects.get(id=vote_id) 

      for choice in choices:
        choice_data = {"text":choice["text"],"vote":vote_instance}
        print(choice_data)
        Choice.objects.create(**choice_data)
        
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({"message":"Postがきちんと呼ばれてます"})
  def create_choices(choices):
    
      return choices

  
