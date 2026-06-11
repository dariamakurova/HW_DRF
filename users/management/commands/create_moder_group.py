from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="moders")
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "moders" успешно создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "moders" уже существует'))
