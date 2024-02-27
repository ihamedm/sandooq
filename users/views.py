from datetime import datetime, timedelta

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.shortcuts import render

from core import settings
from core.helpers import admin_display_jdatetime, display_jdatetime_no_day
from loans.models import Installment, Loan
from users.models import Share


@login_required
def user_dashboard(request):
    user = request.user
    first_unpaid_installments = []
    next_paid_amount = 0
    total_loans_amount = 0
    unpaid_installments_amount = 0
    total_loans_checkouted = 0
    loans = Loan.objects.filter(share__owner=user)
    monthly_fix_amount_assets = settings.MONTHLY_ASSETS_AMOUNT

    shares = Share.objects.filter(owner=user)

    for loan in loans:
        installments = loan.installment_set.all().order_by('due_date')

        # prepare next payment data
        unpaid_installments = loan.installment_set.filter(paid=False).order_by('due_date')

        for installment in unpaid_installments:
            unpaid_installments_amount += installment.amount

        if unpaid_installments.exists():
            first_unpaid_installment = unpaid_installments.first()
            next_paid_amount += first_unpaid_installment.amount
            first_unpaid_installments.append(first_unpaid_installment)


        # Modify installment data as needed
        for installment in installments:
            installment.due_date = display_jdatetime_no_day(installment.due_date)

        # Assign the modified installments back to the loan
        loan.modified_installments = installments

        total_loans_amount += loan.amount
        if loan.checkout:
            total_loans_checkouted += 1

    report_data = {
        'shares': shares,
        'share_asset': shares[0].asset,
        'total_loans_amount': total_loans_amount,
        'unpaid_installments_amount': unpaid_installments_amount,
        'total_loans_checkouted': total_loans_checkouted,
    }

    context = {
        'shares': shares,
        'monthly_fix_amount_assets': monthly_fix_amount_assets,
        'first_unpaid_installments': first_unpaid_installments,
        'next_paid_amount': next_paid_amount + (shares.count() * monthly_fix_amount_assets),
        'loans': loans,
        'user_data': {'firstname': f'{user.first_name}', 'lastname': f'{user.last_name}'},
        'report_data': report_data
    }

    # Render the template with the data
    return render(request, 'front/dashboard.html', context)


def user_logout(request):
    logout(request)
    # Redirect to the home page or any other page after logout
    return redirect('user_dashboard')
