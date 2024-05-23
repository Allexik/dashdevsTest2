from datetime import datetime

from django.db.models import Sum, Case, When, Q, DecimalField
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from payment.api.serializers import BalanceSerializer, TransactionSerializer
from payment.models import Balance, Transaction


class BalanceViewSet(viewsets.ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=['get'], url_path='balance-change')
    def balance_change(self, request, *args, **kwargs):
        balance = self.get_object()
        from_date = request.query_params.get('from_date', '1970-01-01')
        to_date = request.query_params.get('to_date', datetime.now().strftime('%Y-%m-%d'))

        queryset = Transaction.objects.filter(
            Q(balance_from=balance) | Q(balance_to=balance),
            created__range=(from_date, to_date)
        ).aggregate(
            total_amount=Sum(
                Case(
                    When(balance_to=balance, then='amount'),
                    default=0,
                    output_field=DecimalField()
                )
            ) - Sum(
                Case(
                    When(balance_from=balance, then='amount'),
                    default=0,
                    output_field=DecimalField()
                )
            )
        )

        total_amount = queryset['total_amount'] or 0

        return Response({'total_amount': total_amount})


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
