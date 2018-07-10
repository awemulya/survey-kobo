from django import forms
from django.forms import CheckboxSelectMultiple, widgets

from .models import Form

TYPE_CHOICES = [(1, 'Napi'), (2, 'Bhumi Sudhar'), (3, 'Malpot')]


class OfficeFormForm(forms.ModelForm):

    class Meta:

        model = Form

        # type = forms.MultipleChoiceField(
        #     required=False,
        #     help_text="Unselect the photos you want to delete",
        #     choices=TYPE_CHOICES,
        #     widget=forms.CheckboxSelectMultiple(attrs={"checked": ""})
        # )

        fields = '__all__'

