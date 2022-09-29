
from asyncio import constants
from datetime import datetime
import re
import uuid
from rest_framework import generics
from rest_framework import viewsets,views,status
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import ProfileSerializer, QuestionDetailPageSerializer,UserSerializer,QuestionResultPageSerializer
from .models import User,Vote,VoteComment,Thread,ThreadComment,Choice,Profile
from rest_framework.response import Response 


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
    #TODO クエリをつけたい

    vote = Vote.objects.all()
    serializer = QuestionDetailPageSerializer(vote, many=True)
    return Response(serializer.data,status=status.HTTP_201_CREATED)
  
  def post(self,request): 
    request_data = request.data
    print("1回目",request_data)
    now = datetime.now()
    date = '{:%Y-%m-%d}'.format(now) 
    request_data.update({"createdAt": date})
    serializer = QuestionDetailPageSerializer(data=request_data)
    print("------------------------------")
    print("2回目",request_data)
    if serializer.is_valid():
      print("validted")
      profile = Profile.objects.get(user=self.request.user) 
      vote_id = str(uuid.uuid4())

      serializer.save(user=profile,id=vote_id,)
      
      vote_instance = Vote.objects.get(id=vote_id) 
      choices = request_data["choices"]
      for choice in choices:
        choice_data = {"text":choice["text"],"vote":vote_instance}
        print(choice_data)
        Choice.objects.create(**choice_data)
        
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      print("エラー")
      print(serializer.errors)
    return Response({"message":"エラー"})
  
 

class VoteDetailAPIView(views.APIView):


    
  def get(self,request,pk):
   

    vote = Vote.objects.filter(pk=pk)
    serializer = QuestionDetailPageSerializer(vote, many=True)
    return Response(serializer.data,status=status.HTTP_201_CREATED)
    pass
  def put(self, request, pk):
    # 匿名投票をいつか実装したい
   
    # requestからuserを取得する
    # pkからvoteを取得する
    # voteのcountにuserを追加する
    # choicesのvoteduserにuserを追加する
    # dataで受け取るのは choiceのid
    #choiceidを受け取り　filterをかけてvoteduserにUserを追加する
    print("------------------------")
    print(request.data["choice"])
    print(request.user)
    print("------------------------")
    # vote = Vote.objects.get(pk=pk)
    # print("投票数",vote.numberOfVotes)
    # user = User.objects.get(pk=request.user)
    # print("ユーザー",user)

    # vote.numberOfVotes.add(user)
    # serializer = QuestionDetailPageSerializer(vote, data=request.data)
    # if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)

    return Response({"message":"Putしました"}, status=status.HTTP_400_BAD_REQUEST)
    
  

  def delete(self, request, pk):
    vote = self.get_object(pk)
    vote.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)