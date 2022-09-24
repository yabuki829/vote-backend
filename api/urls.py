from django.urls import path,include
from .views import ChoiceViewSets, CreateUserView, ProfileViewSets, VoteViewSet
from rest_framework.routers import DefaultRouter
app_name = 'user'

router = DefaultRouter()
router.register('vote', VoteViewSet)
router.register('profile',ProfileViewSets)
router.register('choice',ChoiceViewSets)

urlpatterns = [
  path('',include(router.urls)),
  path('register/', CreateUserView.as_view(), name='register'),
]
