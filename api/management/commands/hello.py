from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

# デプロイと同時に実行したいコマンドがCommandsファイルに書く
class Command(BaseCommand):
    def handle(self, *args, **options):
      print("hello world")