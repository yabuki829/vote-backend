
from django.urls import path,include
from .views import  CommentThreadPIView, CommentVoteAPIView, CreateUserView, ProfileAPIView, ProfileViewSets, ThreadAPIView, ThreadVoteAPIView,VoteAPIView,VoteDetailAPIView
from rest_framework.routers import DefaultRouter
app_name = 'user'

# router = DefaultRouter()
# router.register('profile',ProfileViewSets)

urlpatterns = [
  path('register/', CreateUserView.as_view(), name='register'),
  path("vote/",VoteAPIView.as_view(),name="vote"),
  
  path("vote/<str:pk>/comment/",CommentVoteAPIView.as_view(),name="commentVote"),
  path("vote/<str:pk>/thread/",ThreadVoteAPIView.as_view(),name="commentVote"),
  path("vote/<str:pk>/",VoteDetailAPIView.as_view(),name="voteDetail"),
  

  
  path("thread/",ThreadAPIView.as_view(),name="thread"),
  path("thread/<str:pk>/comment",CommentThreadPIView.as_view(),name="commentThread"),
  path("thread/<str:pk>/",VoteDetailAPIView.as_view(),name="voteDetail"),
  
  path("profile/",ProfileAPIView.as_view(),name="profile"),

]
