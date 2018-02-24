from django.conf.urls import include, url
from django.conf import settings
import django.views
from rest_framework.routers import DefaultRouter

from rest_api.views import (
    GroupViewSet, UserViewSet, MORouterViewSet, SMPPCCMViewSet, HTTPCCMViewSet, MTRouterViewSet, FiltersViewSet
)

router = DefaultRouter()
router.register(r'groups', GroupViewSet, base_name='groups')
router.register(r'users', UserViewSet, base_name='users')
router.register(r'morouters', MORouterViewSet, base_name='morouters')
router.register(r'mtrouters', MTRouterViewSet, base_name='mtrouters')
router.register(r'smppsconns', SMPPCCMViewSet, base_name='smppcons')
router.register(r'httpsconns', HTTPCCMViewSet, base_name='httpcons')
router.register(r'filters', FiltersViewSet, base_name='filters')

urlpatterns = [
    url(r'^api/', include(router.urls)),
]


if settings.SHOW_SWAGGER:
    urlpatterns += [url(r'^docs/', include('rest_framework_swagger.urls'))]
    urlpatterns += [url(r'^static/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT})]

