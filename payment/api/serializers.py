from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from payment.models import Balance, Transaction


class BalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Balance
        fields = '__all__'


def greater_than_zero(value):
    if value <= 0:
        raise ValidationError('Amount must be greater than 0.')


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[greater_than_zero])

    class Meta:
        model = Transaction
        fields = '__all__'

    def validate(self, attrs):
        balance_from = attrs['balance_from']
        balance_to = attrs['balance_to']
        amount = attrs['amount']

        if balance_from.amount < amount:
            raise ValidationError('Balance from does not have enough amount.')

        if balance_from == balance_to:
            raise ValidationError('Balance from and balance to cannot be the same.')

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        balance_from = validated_data['balance_from']
        balance_to = validated_data['balance_to']
        amount = validated_data['amount']
        balance_from.amount -= amount
        balance_to.amount += amount
        balance_from.save()
        balance_to.save()

        return Transaction.objects.create(**validated_data)
