from django import template


register = template.Library()


@register.filter(name="submission_count")
def submission_count(form, office_id, force_update=False):
    from onadata.apps.office.models import OfficeInstance
    count = OfficeInstance.objects.filter(office_id=office_id, instance__xform_id=form.xform.id).count()
    return count

