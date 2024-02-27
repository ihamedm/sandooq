from django.db import models
from django.utils.translation import gettext as _
from loans.models import Installment


class BankAccount(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    shaba_number = models.CharField(max_length=26, null=True, blank=True, help_text='با IR بنویسید')

    def __str__(self):
        return self.name


class Transaction(models.Model):
    transaction_type_choices = [
        ('deposit', _('Deposit')),
        ('withdrawal', _('Withdrawal'))
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    bank_account = models.ForeignKey('finance.BankAccount', on_delete=models.PROTECT, null=True, blank=True)
    bank_balance = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, editable=False)
    transaction_type = models.CharField(max_length=10, choices=transaction_type_choices)
    date = models.DateTimeField(auto_now_add=True)
    installments = models.ManyToManyField('loans.Installment', blank=True, verbose_name=_('also checkout these Installments:'))
    share_assets = models.ManyToManyField('users.Share', blank=True, verbose_name=_('Shares to increase assets'))
    notes = models.CharField(max_length=100, null=True, blank=True)
    accounting_done = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.amount}'

    def save(self, *args, **kwargs):
        self.update_bank_account_balance()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Update the bank account balance for deleted transactions
        self.update_bank_account_balance(delete=True)
        super().delete(*args, **kwargs)

    def update_bank_account_balance(self, delete=False):
        global amount_change
        if self.bank_account:
            if self.transaction_type == 'deposit':
                amount_change = self.amount if not delete else -self.amount
            elif self.transaction_type == 'withdrawal':
                amount_change = -self.amount if not delete else self.amount

            self.bank_account.balance += amount_change
            self.bank_account.save()

            # Update the bank balance field
            if not self.bank_balance:
                self.bank_balance = self.bank_account.balance + amount_change
            else:
                self.bank_balance += amount_change
        else:
            self.bank_balance = 0


