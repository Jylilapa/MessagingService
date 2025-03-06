from django.core.management import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


class Command(BaseCommand):
    def handle(self, *args, **options):
        manager_group = Group.objects.create(name='Менеджеры')
        list_permission = Permission.objects.get(codename='can_view_list_recipients')
        mailings_list_permission = Permission.objects.get(codename='can_view_list_mailings')
        stop_permission = Permission.objects.get(codename='can_stop_mailings')
        user_list_permission = Permission.objects.get(codename='can_view_list_users')
        user_block_permission = Permission.objects.get(codename='can_block_user')
        manager_group.permissions.add(list_permission, mailings_list_permission, stop_permission, user_list_permission, user_block_permission)

