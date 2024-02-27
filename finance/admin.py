from django.contrib import admin
from django.shortcuts import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext as _

from core.helpers import admin_display_jdatetime
from finance.models import Transaction, BankAccount


@admin.register(BankAccount)
class BankAccountModelAdmin(admin.ModelAdmin):
    model = BankAccount
    list_display = ['name', 'balance']


@admin.register(Transaction)
class TransactionModelAdmin(admin.ModelAdmin):
    model = Transaction

    list_display = ['user', 'bank_account', 'jdate', 'notes', 'amount_display', 'bank_balance', 'do_accounting']
    list_filter = ['bank_account', 'transaction_type']
    # autocomplete_fields = ['installments']

    fieldsets = (
        (None, {'fields': ('user', 'transaction_type', 'amount', 'bank_account',)}),
        (_('Auto accounting'), {'fields': ('installments', 'share_assets')}),
        (_('info'), {'fields': ('notes', 'accounting_done')}),
    )

    class Media:
        js = ('js/transaction.js',)

    @admin.display(description=_('Date'))
    def jdate(self, obj):
        return admin_display_jdatetime(obj.date)

    @admin.display(description=_('Amount'))
    def amount_display(self, obj):
        if obj.transaction_type == 'deposit':
            return format_html('<span style="color:green">&#x25B2;{}</span>', obj.amount)
        elif obj.transaction_type == 'withdrawal':
            return format_html('<span style="color:red">&#x25BC;{}</span>', obj.amount)
        else:
            return obj.transaction_type

    @admin.display(description=_('Balance'))
    def bank_balance(self, obj):
        # Fetch the bank balance for the transaction's bank account
        bank_account = obj.bank_account
        if bank_account:
            transactions = Transaction.objects.filter(bank_account=bank_account, date__lte=obj.date)
            balance = bank_account.balance
            # Calculate the balance by iterating over transactions and adjusting it based on transaction type
            for transaction in transactions:
                if transaction.transaction_type == 'deposit':
                    balance += transaction.amount
                elif transaction.transaction_type == 'withdrawal':
                    balance -= transaction.amount
            return balance
        return ''

    @admin.display(description=_('Do accounting'))
    def do_accounting(self, obj):
        url = reverse('mark_installments_as_paid')
        params = urlencode({'transaction_id': obj.id})
        if obj.accounting_done:
            return format_html('<button class="button disabled" disabled>Done</button>')
        else:
            return format_html('<a href="#" class="mark-as-paid button" data-url="{}?{}">Do Accounting</a>', url, params)
