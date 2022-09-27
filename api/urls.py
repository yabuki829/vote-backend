
from django.urls import path,include
from .views import  CreateUserView, ProfileViewSets,VoteAPIView,VoteDetailAPIView
from rest_framework.routers import DefaultRouter
app_name = 'user'

router = DefaultRouter()
router.register('profile',ProfileViewSets)

urlpatterns = [
  path('',include(router.urls)),
  path('register/', CreateUserView.as_view(), name='register'),
  path("vote/",VoteAPIView.as_view(),name="vote"),
  path("vote/<str:pk>/",VoteDetailAPIView.as_view(),name="voteDetail")
]
