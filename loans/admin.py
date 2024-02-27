from django.contrib import admin
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from core import settings
from core.helpers import admin_display_jdatetime
from finance.models import Transaction
from loans.models import Loan, Installment


# Register your models here.

@admin.register(Loan)
class LoanModelAdmin(admin.ModelAdmin):
    model = Loan
    ordering = ['paid_date']
    list_filter = ['share']
    search_fields = ['share__owner__first_name', 'share__owner__last_name']
    list_display = ['share', 'amount', 'installments', 'installment_amount', 'unpaid_amount', 'number', 'paid_date', 'checkout', 'view_installments']

    def unpaid_amount(self, obj):
        paid_installments_amount = obj.installment_set.filter(paid=True).aggregate(total_amount=Sum('amount'))[
                                       'total_amount'] or 0
        remaining_unpaid_amount = obj.amount - paid_installments_amount
        return remaining_unpaid_amount

    def view_installments(self, obj):
        url = reverse('admin:loans_installment_changelist') + f'?loan__id__exact={obj.id}'
        return mark_safe(f'<a href="{url}" class="button">{_("Installments")}</a>')

    class Media:
        js = ('js/loan.js',)


@admin.register(Installment)
class InstallmentModelAdmin(admin.ModelAdmin):
    model = Installment
    ordering = ['due_date']
    list_filter = ['loan', 'share']
    search_fields = ['share__owner__first_name', 'share__owner__last_name']
    list_editable = ['paid']

    @admin.display(description='تاریخ سررسید')
    def jdue_date(self, obj):
        return admin_display_jdatetime(obj.due_date)

    @admin.display(description='تاریخ پرداخت')
    def jpaid_date(self, obj):
        return admin_display_jdatetime(obj.paid_date) if obj.paid_date else '-'

    list_display = ['loan', 'share', 'installment_number', 'amount', 'paid', 'jdue_date', 'jpaid_date']



