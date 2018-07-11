from django.core.management.base import BaseCommand

import sys
import argparse
import pandas as pd
from onadata.apps.office.models import Office, District


class Command(BaseCommand):
    help = 'Create default office from district xlsx file'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType())

    def handle(self, *args, **options):
        df = pd.read_excel(sys.argv[3])
        office = [
            Office(
                    name=df['Office Name'][row],
                    district=District.objects.get(id=20),
                    type=df['Office Type'][row],

            ) for row in range(0, 225)
        ]
        office = Office.objects.bulk_create(office)
        if office:
            self.stdout.write('Successfully created offices ..')

