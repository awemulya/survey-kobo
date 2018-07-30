from django.core.management.base import BaseCommand

from onadata.apps.office.models import Type


class Command(BaseCommand):
    help = 'Create office types'

    def handle(self, *args, **options):
		type_choices = [1, 2, 3]
		for type in type_choices:
			Type.objects.get_or_create(type=type)
		self.stdout.write("Successfully created office types")