
import uuid
from rest_framework import generics
from rest_framework import viewsets,views,status
from rest_framework.permissions import AllowAny
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
    serializer = QuestionDetailPageSerializer(data=request_data)
    
    if serializer.is_valid():
      profile = Profile.objects.get(user=self.request.user) 
      vote_id = str(uuid.uuid4())
      serializer.save(user=profile,id=vote_id)
      
      vote_instance = Vote.objects.get(id=vote_id) 
      choices = request_data["choices"]
      for choice in choices:
        choice_data = {"text":choice["text"],"vote":vote_instance}
        print(choice_data)
        Choice.objects.create(**choice_data)
        
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({"message":"エラー"})


  
