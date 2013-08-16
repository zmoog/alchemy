from rest_framework import serializers
from cash.models import Account, Transfer


class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		#fields = ('name', 'type')
			

class TransferSerializer(serializers.ModelSerializer):

	source = AccountSerializer()
	destination = AccountSerializer()

	class Meta:
		model = Transfer
		#fields = ('amount', 'source', 'destination',)
			
