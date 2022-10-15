from urllib.request import Request
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework import serializers
from .models import User,Vote,VoteComment,Thread,ThreadComment,Choice,Profile
from django.contrib.auth import get_user_model



class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "email","password"]
    extra_kwargs= {'password': {'write_only': True},'email': {'write_only': True}}

  def create(self ,validated_data):
    print("作成")
    user = get_user_model().objects.create_user(**validated_data)
              # User.objects.create_user(request_data=validated_data)
    return user 

class ProfileSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  class Meta:
    model = Profile
    fields = ["id","nickName","user","createdAt","image"]
    extra_kwargs = {'user': {'read_only': True}}

 
class ChoiceSerializer(serializers.ModelSerializer):
  votedUserCount = UserSerializer(read_only=True,many=True)
  id = serializers.UUIDField(read_only=True)
  text = serializers.CharField(max_length=200)

  class Meta:
    model = Choice
    fields = ["id","text","votedUserCount"]
    extra_kwargs = {'user': {'read_only': True}}
  
  def create(self, validated_data):
      print("Choiceを作成します")
      return Choice.objects.create(**validated_data)

class VoteSerializer(serializers.ModelSerializer):
  createdAt = serializers.DateTimeField(format="%Y年%m月%d日", read_only=True)
  user = ProfileSerializer(read_only=True)
  choices = ChoiceSerializer()
  numberOfVotes = UserSerializer(read_only=True,many=True)
  class Meta:
    model = Vote
    fields = ["id","user","questionText","createdAt","image","isOnlyLoginUser","choices","numberOfVotes"]
    extra_kwargs = {'user': {'read_only': True}}
  

  def create(self, validated_data):
    return Vote.objects.create(**validated_data)
    
class ChoiceSerializerWithVotes(ChoiceSerializer):
    votes = serializers.UUIDField(read_only=True)

class QuestionDetailPageSerializer(VoteSerializer):
  choices = ChoiceSerializer(many=True, read_only=True)
  
class QuestionResultPageSerializer(VoteSerializer):
  choices = ChoiceSerializerWithVotes(many=True, read_only=True)

  


#TODO スレッド　コメントのシリアライザーを作成する

class VoteThreadSerializer(serializers.ModelSerializer):
  createdAt = serializers.DateTimeField(format="%Y年%m月%d日", read_only=True)
  user = ProfileSerializer(read_only=True)
  choices = ChoiceSerializer(read_only=True,many=True)
  numberOfVotes = UserSerializer(read_only=True,many=True)
  class Meta:
    model = Vote
    fields = ["id","user","questionText","createdAt","image","isOnlyLoginUser","choices","numberOfVotes"]
    extra_kwargs = {'user': {'read_only': True}}



class ThreadSerializer(serializers.ModelSerializer):
  createdAt = serializers.DateTimeField(format="%Y年%m月%d日", read_only=True)
  vote = VoteThreadSerializer()
  user = ProfileSerializer(read_only=True)
  class Meta:
    model = Thread
    fields = ["id","user","vote","title","createdAt"]
    extra_kwargs = {'user': {'read_only': True}}

class ThreadCommentSerializer(serializers.ModelSerializer):
  createdAt = serializers.DateTimeField(format="%Y年%m月%d日", read_only=True)
  user = ProfileSerializer()
  class Meta:
    model = ThreadComment
    fields = ["id","user","text","createdAt"]


class VoteCommentSerializer(serializers.ModelSerializer):
  createdAt = serializers.DateTimeField(format="%Y年%m月%d日", read_only=True)
  user = ProfileSerializer()
  class Meta:
    model = VoteComment
    fields = "__all__"
