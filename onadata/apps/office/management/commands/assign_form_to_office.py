from django.core.management.base import BaseCommand

import sys
import argparse
import pandas as pd
from onadata.apps.office.models import Form
from onadata.apps.logger.models import XForm


class Command(BaseCommand):
    help = 'Assign form to offices'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType())

    def handle(self, *args, **options):
        df = pd.read_excel(sys.argv[3])
        count=df['XFormId'].count()
        # import ipdb;ipdb.set_trace()
        forms = [
            Form(
                    xform=XForm.objects.get(id_string=df['XFormId'][row]),
                    type=[df['Type'][row]],
                    anusuchi=str(df['Anusuchi'][row]),

            ) for row in range(0, count)
        ]
        forms = Form.objects.bulk_create(forms)
        if forms:
            self.stdout.write('Successfully assigned forms to offices ..')

