
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

class ProfileViewSets(viewsets.ModelViewSet):
  queryset = Profile.objects.all()
  serializer_class = ProfileSerializer

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)


class ChoiceViewSets(viewsets.ModelViewSet):
  print("ChoiceViewSetsが呼ばれました")
  queryset = Choice.objects.all()
  serializer_class = ChoiceSerializerWithVotes


  def perform_create(self,serializer,id):
    print("---------------------------------")
    print("perform_create作成されました。")
    print("serializer1",serializer)
    serializer.save(vote=id)


class VoteViewSet(viewsets.ModelViewSet):
  print("VoteViewSetが呼ばれました")
  queryset = Vote.objects.all()
  serializer_class = QuestionResultPageSerializer

  def create(self, request, *args, **kwargs):
   
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    choices = request.data["choices"]
    self.perform_create(serializer,choices)
    #---------------------------------
    # TODO 返却値にChicesのデータを含ませたい

    #選択肢を作成するコード
    #serializeにもこれをどうにか反映させたい
    #perform_createをこのコードより上で実装しているから
    #headers = self.get_success_headers(serializer.data)　
    ##　で返却するserializer.dataにはchice空になる

    vote_id = serializer.data["id"]
    vote_instance = Vote.objects.get(id=vote_id) 
   
    for choice in choices:
      choice_data = {"text":choice["text"],"vote":vote_instance}
      Choice.objects.create(**choice_data)
      
    # choice_dic = Choice.objects.filter(vote=vote_instance)
    # print("-------------------------")
    # print("choice_dic")
    # print(choice_dic)
    # print("-------------------------")
    # print("is_validする")
   
    #---------------------------------
    
    
    headers = self.get_success_headers(serializer.data)

    
    return  Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
  
  def perform_create(self,serializer,choices):
   
    profile = Profile.objects.get(user=self.request.user)
    vote_id = str(uuid.uuid4())
    
    # vote_instance =Vote.objects.create(id=vote_id,user=profile)
    # print("--------------")
    # print("これ",choices)
    # for choice in choices :
    #   Choice.objects.create(**choice,vote=vote_instance)
      
    serializer.save(user=profile,id=vote_id)
    #　ここでChoiceを登録したい

    
  
  


  
