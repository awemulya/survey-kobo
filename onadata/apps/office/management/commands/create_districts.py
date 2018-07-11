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
        districts = df['District Name'].unique()
        for district in districts:
            District.objects.get_or_create(name=district)


