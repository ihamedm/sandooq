from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from finance.models import Transaction


# @receiver(post_save, sender=Transaction)
def transaction_auto_accounting(sender, instance, created, **kwargs):
    if instance.transaction_type == 'deposit':
        installments = instance.installments.all()

        for installment in installments:
            print(installment)
            installment.paid = True
            installment.save()

