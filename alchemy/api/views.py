from rest_framework import viewsets
from rest_framework import generics
from api.serializers import AccountSerializer, TransferSerializer
from cash.models import Account, Transfer


class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransferViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Transfer.objects.all().order_by('-validity_date')
    serializer_class = TransferSerializer
