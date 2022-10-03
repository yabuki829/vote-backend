
from concurrent.futures import thread
from secrets import choice
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.conf import settings
import uuid


class UserManager(BaseUserManager):
  def create_user(self,email,password=None):
    if not email:
      raise ValueError("Email is must")
    # Normalizes email addresses by lowercasing the domain portion of the email address. してる
    user = self.model(email=self.normalize_email(email))
    # Sets the user’s password to the given raw string, taking care of the password hashing. Doesn’t save the User object.
    # https://docs.djangoproject.com/en/4.1/ref/contrib/auth/ 
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self,email,password):
    user = self.create_user(email,password)
    # https://docs.djangoproject.com/en/4.1/topics/auth/customizing/ Custom users and django.contrib.adminのところ
    
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)

    return user

class User(AbstractBaseUser,PermissionsMixin):
  id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
  email = models.EmailField(max_length=100,unique=True)
  is_active =  models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserManager()
  USERNAME_FIELD = "email"

  def __str__(self):
      return self.email
  
def upload_profile_image_path(instance, filename):
    #jpg png などの拡張子の部分を取得する
    ext = filename.split('.')[-1]
    return '/'.join(['images/profiles',str(instance.user.id)+str(uuid.uuid4)+str(".")+str(ext)])

def upload_post_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['images/posts', str(instance.userPost.id)+str(uuid.uuid4)+str(".")+str(ext)])

class Profile(models.Model):
  id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
  nickName = models.CharField(max_length=20,default="No Name")
  user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name="user",on_delete=models.CASCADE)
  createdAt = models.DateTimeField(auto_now_add=True) 
  image = models.ImageField(blank=True, null=True, upload_to=upload_profile_image_path)
  def __str__(self):
      return self.nickName

class Vote(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    questionText = models.CharField(max_length=200)
    createdAt = models.DateTimeField(auto_now_add=True) 
    image = models.ImageField(blank=True, null=True, upload_to=upload_profile_image_path)
    #ログインしているアカウントのみ投票できる
    isOnlyLoginUser = models.BooleanField(default=False)
    numberOfVotes = models.ManyToManyField(User, blank=True)
    def __str__(self) -> str:
       return self.questionText

class Choice(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=200)
    #誰がこの選択肢に投票したのか
    votedUserCount = models.ManyToManyField(User, blank=True)
    vote = models.ForeignKey(Vote,blank=True,on_delete=models.CASCADE,related_name="choices") 
    def __str__(self) -> str:
       return self.text


  

class Thread(models.Model):
  user = models.ForeignKey(Profile, on_delete=models.CASCADE)
  vote = models.ForeignKey(Vote, blank=True, on_delete=models.CASCADE )
  title = models.CharField(max_length=100)
  createdAt = models.DateTimeField(auto_now_add=True) 
  def __str__(self) -> str:
       return self.title


class ThreadComment(models.Model):
  user = models.ForeignKey(Profile, on_delete=models.CASCADE)
  thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
  text = models.CharField(max_length=100)
  createdAt = models.DateTimeField(auto_now_add=True) 
  

  def __str__(self) -> str:
       return self.text



class VoteComment(models.Model):
  user = models.ForeignKey(Profile, on_delete=models.CASCADE)
  vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
  text = models.CharField(max_length=100)
  createdAt = models.DateTimeField(auto_now_add=True) 
  def __str__(self) -> str:
       return  self.text