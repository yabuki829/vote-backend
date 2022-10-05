
from datetime import datetime
import uuid
from rest_framework import generics
from rest_framework import viewsets,views,status
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import ProfileSerializer, QuestionDetailPageSerializer, ThreadSerializer,UserSerializer,QuestionResultPageSerializer
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
    


  

class VoteAPIView(views.APIView):
  permission_classes = [AllowAny,]
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
    pass

  def delete(self, request, pk):
    pass