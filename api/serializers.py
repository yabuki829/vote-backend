
from secrets import choice
from rest_framework import serializers
from .models import User,Vote,VoteComment,Thread,ThreadComment,Choice,Profile
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ["id", "email"]
    extra_kwargs= {'password': {'write_only': True}}

  def create(self ,validated_data):
      user = get_user_model().objects.create_user(**validated_data)
              # User.objects.create_user(request_data=validated_data)
      return user 

class ProfileSerializer(serializers.ModelSerializer):
  createdAt = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
  user = UserSerializer(read_only=True)
  class Meta:
    model = Profile
    fields = ["id","nickName","user","createdAt","image"]
    extra_kwargs = {'user': {'read_only': True}}

class ChoiceSerializer(serializers.ModelSerializer):
  votedUserCount = ProfileSerializer(many=True)
  print("ChoiceSerializerが呼ばれました")
  class Meta:
    model = Choice
    fields = ["id","text","votedUserCount"]
    extra_kwargs = {'user': {'read_only': True}}

class VoteSerializer(serializers.ModelSerializer):
  createdAt = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
  user = ProfileSerializer(read_only=True)
  choices = ChoiceSerializer(read_only=True,many=True)

  class Meta:
    model = Vote
    fields = ["id","user","questionText","createdAt","image","isOnlyLoginUser","choices"]
    extra_kwargs = {
      'user': {'read_only': True},
      }
    

    

class VoteCommentCommentSerializer(serializers.ModelSerializer):
  createdAt = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
  class Meta:
    model = VoteComment
    fields = ["id","user","vote","text","createdAt"]
    






class ThreadSerializer(serializers.ModelSerializer):
  createdAt = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
  class Meta:
    model = Thread
    fields = ["id","user","vote","title","createdAt"]
    # extra_kwargs = {'user': {'read_only': True}}

class ThreadCommentSerializer(serializers.ModelSerializer):
  createdAt = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
  class Meta:
    model = ThreadComment
    fields = ["id","user","thread","text","createdAt"]
    # extra_kwargs = {'user': {'read_only': True}}


 