from django.urls import path, include
from rest_framework import routers

from project_db_api.views import *

router = routers.DefaultRouter()
router.register('main_analytic', Main_analytic_ViewSet)
router.register('supplies_info', Supplies_info_ViewSet)
router.register('abc', ABC_ViewSet)


urlpatterns = [
    path('', include(router.urls)),
]