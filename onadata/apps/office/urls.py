from django.conf.urls import url, include

from rest_framework import routers

from .views import*
from .viewsets import*


router = routers.DefaultRouter()

router.register(r'office', OfficeViewset)
router.register(r'office-users', OfficeUserViewset)
router.register(r'users', UserViewset)
router.register(r'office-forms', OfficeFormViewset)
router.register(r'forms', FormViewset)
router.register(r'xforms', XFormViewset)
router.register(r'districts', DistrictViewset)
router.register(r'type', TypeViewset)

urlpatterns = [
    # url(r'^', Application.as_view(), name='home'),
    url(r'api/',  include(router.urls)),
    url('api-token-auth/', token),

    url(r'enketo1/(?P<pk>[\d+^/]+)/(?P<office>[\d+^/]+)', get_enketo_survey_links, name='links'),
    url('assigned-forms-list/(?P<office_id>[\d+^/]+)', OfficeFormListViewset.as_view({'get': 'list', }), name="office_forms"),

    url(r'/dashboard/$', Dashboard.as_view(), name='dashboard'),
    url(r'/office-detail/(?P<pk>[\d+^/]+)/$', OfficeDetailView.as_view(), name='office_detail'),
    url(r'/xform-create/$', XFormView.as_view(), name='xform'),
    url(r'/form-create/$', FormView.as_view(), name='form'),


]
