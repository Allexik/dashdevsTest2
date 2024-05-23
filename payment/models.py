from django.core.exceptions import ValidationError
from django.db import models


class Balance(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Transaction(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_from = models.ForeignKey(Balance, on_delete=models.CASCADE, related_name='balance_from')
    balance_to = models.ForeignKey(Balance, on_delete=models.CASCADE, related_name='balance_to')

    def clean(self):
        if self.balance_from == self.balance_to:
            raise ValidationError("balance_from and balance_to cannot be the same.")

        if self.amount < 0:
            raise ValueError("Transaction amount should be greater than 0. Current amount is {}".format(self.amount))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
