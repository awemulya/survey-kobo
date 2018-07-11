from django.core.management.base import BaseCommand

import sys
import argparse
import pandas as pd
from onadata.apps.office.models import District


class Command(BaseCommand):
    help = 'Create default districts from district xlsx file'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType())

    def handle(self, *args, **options):
        df = pd.read_excel(sys.argv[3])
        district = [
            District(
                    name=df['District Name'][row],

            ) for row in range(0, 225)
        ]
        district = District.objects.bulk_create(district)
        if district:
            self.stdout.write('Successfully created districts ..')

