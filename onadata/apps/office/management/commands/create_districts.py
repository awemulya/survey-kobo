from django.core.management.base import BaseCommand

from onadata.apps.office.models import District


class Command(BaseCommand):
    help = 'Create default districts'

    def handle(self, *args, **options):
        districts_list = ["Kathmandu",
                          "Lalitpur",
                          "Bhaktapur",
                          "Jhapa",
                          "Morang",
                          "Sunsari",
                          "Illam",
                          ]
        for district in districts_list:
            new_district, created = District.objects.get_or_create(name=district)
            if created:
                self.stdout.write('Successfully created districts.. "%s"' % new_district)