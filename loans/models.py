from django.db import models
from core.helpers import admin_display_jdatetime


class Loan(models.Model):
    share = models.ForeignKey('users.Share', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    bank_account = models.ForeignKey('finance.BankAccount', on_delete=models.PROTECT)
    installments = models.IntegerField()
    installment_amount = models.DecimalField(max_digits=12, decimal_places=0)
    last_installment_amount = models.DecimalField(max_digits=12, decimal_places=0)
    number = models.IntegerField(default=0)
    paid_date = models.DateTimeField(auto_now=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    checkout = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.share.__str__()} - {self.amount}'


class Installment(models.Model):
    loan = models.ForeignKey('loans.Loan', on_delete=models.CASCADE)
    share = models.ForeignKey('users.Share', on_delete=models.CASCADE)
    installment_number = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    paid_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    notes = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.share} - {self.amount} [ {admin_display_jdatetime(self.due_date)} ]'
