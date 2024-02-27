from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from core import settings
from finance.models import Transaction


@require_POST
def mark_installments_as_paid(request):
    transaction_id = request.GET.get('transaction_id')
    try:
        transaction = Transaction.objects.get(id=transaction_id)

        if transaction.transaction_type == 'deposit':
            installments_res = transaction.installments.all().update(paid=True, paid_date=timezone.now())

            for share_asset in transaction.share_assets.all():
                share_asset.asset += settings.MONTHLY_ASSETS_AMOUNT
                share_asset.save()

            transaction.accounting_done = True
            transaction.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': True})
    except Transaction.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Transaction not found'})