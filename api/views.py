
from concurrent.futures import thread
from datetime import datetime
from secrets import choice
import uuid
from requests import request
from rest_framework import generics
from rest_framework import viewsets,views,status
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import ProfileSerializer, QuestionDetailPageSerializer, ThreadCommentSerializer, ThreadSerializer,UserSerializer,QuestionResultPageSerializer, VoteCommentSerializer, VoteSerializer
from .models import User,Vote,VoteComment,Thread,ThreadComment,Choice,Profile
from rest_framework.response import Response 


class CreateUserView(generics.CreateAPIView):
  serializer_class = UserSerializer
  permission_classes = [AllowAny,]

  def perform_create(self, serializer):
    print("ユーザーを作成します")
    return super().perform_create(serializer)

class ProfileViewSets(viewsets.ModelViewSet):
  queryset = Profile.objects.all()
  serializer_class = ProfileSerializer

  def perform_create(self, serializer):
    if Profile.objects.filter(user=self.request.user).exists() == False:
      serializer.save(user=self.request.user)

    
class ProfileAPIView(views.APIView):
  permission_classes = [AllowAny,]

  #一覧ではなく自分のprofileを取得する
  def get(self,request):
    print(self.request.user)
    # profile = Profile.objects.all()
    profile = Profile.objects.filter(user=self.request.user)
    serializer = ProfileSerializer(profile, many=True)
    return Response(serializer.data,status=status.HTTP_201_CREATED)

  def post(self,request):
    Profile.objects.create(user=self.request.user)
    profile = Profile.objects.filter(user=self.request.user)
    serializer = ProfileSerializer(profile, many=True)
    return Response(serializer.data,status=status.HTTP_201_CREATED)

  def fetch():
    pass

  

class VoteAPIView(views.APIView):
  permission_classes = [AllowAny,]
  def get(self,request):
    #TODO クエリをつけたい

    vote = Vote.objects.order_by('-createdAt')
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
  permission_classes = [AllowAny,]
  def get(self,request,pk):
   

    vote = Vote.objects.filter(pk=pk)
    serializer = QuestionDetailPageSerializer(vote, many=True)
    return Response(serializer.data,status=status.HTTP_201_CREATED)

    pass
  def put(self, request, pk):
   
    #pkからvoteを取得する
    vote_id = pk
    vote_data = Vote.objects.get(id=vote_id) 
 
    #voteのnumberOfVotesにuserを追加する
    user = self.request.user
    vote_data.numberOfVotes.add(user)
    vote_data.save()


    choiceID = request.data 
    choice_data = Choice.objects.get(id=choiceID)
    # ユーザーでなくプロフィールである理由は
    # 誰がこの選択肢に対して投稿したか質問者は確認できる様にするため。
    choice_data.votedUserCount.add(user)
    choice_data.save()
    return Response({"message":"PUTしました"})
  

  def delete(self, request, pk):
    vote = self.get_object(pk)
    vote.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



class ThreadAPIView(views.APIView):
  permission_classes = [AllowAny,]
  
  def get(self,request):
    thread = Thread.objects.all()
    serializer = ThreadSerializer(thread,many=True)
    return Response(serializer.data,status=status.HTTP_201_CREATED)

  def post(self,request): 
    print("000000000000000000000000000000")
    print("スレッドを作成します")
    print(self.request.data["vote_id"])
    print(self.request.data["thread_title"])
    user = Profile.objects.get(user=self.request.user)
    print(user)
    vote = Vote.objects.get(pk=self.request.data["vote_id"])
    Thread.objects.create(user=user,vote=vote,title=self.request.data["thread_title"])

    thread = Thread.objects.all()
    serializer = ThreadSerializer(thread,many=True)
    return Response(serializer.data,status=status.HTTP_201_CREATED)

  def delete(self, request, pk):
    pass



import json
from django.forms.models import model_to_dict

#Voteに対するコメント
class CommentVoteAPIView(views.APIView):
  permission_classes = [AllowAny,]

  def get(self,request,pk):
    print(pk,"のvoteのコメントを取得する")
    comment = VoteComment.objects.order_by('-createdAt').filter(vote=pk)
    serializer = VoteCommentSerializer(comment,many=True)
    return Response(serializer.data,status=status.HTTP_201_CREATED)
  

  def post(self,request,pk):
    print(pk,"のvoteにコメントを追加する")
    request_data = self.request.data 
    now = datetime.now()
    date = '{:%Y-%m-%d}'.format(now) 

    vote_instance =  Vote.objects.get(pk=pk)
    profile_instance = Profile.objects.get(user=self.request.user)
    id = uuid.uuid4() 
    request_data.update(
        {
          "id":id,
          "createdAt": date,
          "vote":vote_instance,
          "user":profile_instance,
        }
      )
    data = VoteComment.objects.create(**request_data)
    
    comment = VoteComment.objects.order_by('-createdAt').filter(vote=pk)
    serializer = VoteCommentSerializer(comment,many=True)
    return Response(serializer.data,status=status.HTTP_201_CREATED)
    
  def delete(self,requset,pk):
    pass

class ThreadVoteAPIView(views.APIView):
    permission_classes = [AllowAny,]
    def get(self,request,pk):
      thread = Thread.objects.order_by('-createdAt').filter(vote=pk)
      serializer = ThreadSerializer(thread,many=True)
      return Response(serializer.data,status=status.HTTP_201_CREATED)
    def post(self,request):

      pass
    def delete():
      pass



#スレッドに対するコメント
class CommentThreadPIView(views.APIView):
  permission_classes = [AllowAny,]


  #pk取得する
  def get(self,request,pk):
    print("----------------------")
    print(pk,"ここです")
    comment = ThreadComment.objects.filter(thread=pk)
    
    print(comment,"取得できてる")
    serializer = ThreadCommentSerializer(comment,many=True)
    return Response(serializer.data,status=status.HTTP_201_CREATED)
   

  def post(self,requset,pk):
    thread = Thread.objects.get(pk=pk)
    user = Profile.objects.get(user=self.request.user)
    print("------------------------------")
    print("コメントを作成します")
    print(self.request.data["text"])
    print("------------------------------")
    ThreadComment.objects.create(thread=thread,text=self.request.data["text"],user=user)
    
    comment = ThreadComment.objects.filter(thread=pk)
    print(comment,"取得できてる")
    serializer = ThreadCommentSerializer(comment,many=True)
    return Response(serializer.data,status=status.HTTP_201_CREATED)
  
  def delete(self,requset,pk):
    pass
