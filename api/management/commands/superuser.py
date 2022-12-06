from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

# デプロイと同時に実行したいコマンドがCommandsファイルに書く
class Command(BaseCommand):
    def handle(self, *args, **options):
        print("呼ばれてる？？？")
        # superuserがなければ新しく作成する
        if not User.objects.filter(email=settings.SUPERUSER_EMAIL).exists():
            user = User.objects.create_superuser(
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD
            )
            user.is_staff = True
            user.is_superuser = True
            print("スーパーユーザー作成")
        else:
          print("スーパーユーザーは存在しているので作成しません")