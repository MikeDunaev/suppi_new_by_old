# Create your views here.
from rest_framework import viewsets
from project_db_api.serializers import *
from rest_framework.permissions import AllowAny


class Main_analytic_ViewSet(viewsets.ModelViewSet):
    """
    Таблица, которая используется для отображения основновных финансовых показателей, привязывается к каждому аккаунту продавца.
    """
    queryset = Main_analytic.objects.all()
    permission_classes = [
        AllowAny
    ]
    serializer_class = Main_analytic_serializer


class Supplies_info_ViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Supplies_info.objects.all()
    permission_classes = [
        AllowAny
    ]
    serializer_class = Supplies_info_serializer


class ABC_ViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ABC.objects.all()
    permission_classes = [
        AllowAny
    ]
    serializer_class = ABC_serializer