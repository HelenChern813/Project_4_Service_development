from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class Command(BaseCommand):
    help = "Создает группу с заданными правами доступа"

    def add_arguments(self, parser):
        parser.add_argument('group_name', type=str, help="Название группы")
        parser.add_argument('app_label', type=str, help="Метка приложения")
        parser.add_argument('model_name', type=str, help="Название модели")
        parser.add_argument('permissions', nargs='+', type=str, help="Список прав (add, change, delete, view)")

    def handle(self, *args, **options):
        group_name = options['group_name']
        app_label = options['app_label']
        model_name = options['model_name']
        permissions = options['permissions']

        # Получаем или создаем группу
        group, created = Group.objects.get_or_create(name=group_name)

        # Получаем контент-тип модели
        content_type = ContentType.objects.get(
            app_label=app_label,
            model=model_name
        )

        # Создаем и добавляем права
        for perm in permissions:
            codename = f"{perm}_{model_name}"
            try:
                permission = Permission.objects.get(
                    codename=codename,
                    content_type=content_type
                )
                group.permissions.add(permission)
                self.stdout.write(self.style.SUCCESS(f"Добавлена пермиссия: {permission.name}"))
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Пермиссия {codename} не существует"))

        self.stdout.write(self.style.SUCCESS(f"Группа {group_name} успешно создана"))
