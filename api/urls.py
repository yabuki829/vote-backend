
from django.urls import path,include
from .views import  CreateUserView, ProfileAPIView, ProfileViewSets, ThreadAPIView,VoteAPIView,VoteDetailAPIView
from rest_framework.routers import DefaultRouter
app_name = 'user'

# router = DefaultRouter()
# router.register('profile',ProfileViewSets)

urlpatterns = [
  path('register/', CreateUserView.as_view(), name='register'),
  path("vote/",VoteAPIView.as_view(),name="vote"),
  path("vote/<str:pk>/",VoteDetailAPIView.as_view(),name="voteDetail"),
  path("thread/",ThreadAPIView.as_view(),name="thread"),
  path("thread/<str:pk>/",VoteDetailAPIView.as_view(),name="voteDetail"),
  path("profile/",ProfileAPIView.as_view(),name="profile"),
]
