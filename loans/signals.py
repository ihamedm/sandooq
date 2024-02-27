from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from finance.models import Transaction
from loans.models import Loan, Installment


@receiver(post_save, sender=Loan)
def create_installments_and_transaction(sender, instance, created, **kwargs):
    if created:
        # create installments of loan
        for i in range(instance.installments):
            next_month = instance.paid_date.replace(day=24) + timedelta(days=30 * (i + 1))
            due_date = next_month.replace(day=24)
            Installment.objects.create(
                loan=instance,
                share=instance.share,
                installment_number=i + 1,
                due_date=due_date,
                amount=instance.installment_amount if i < instance.installments - 1 else instance.last_installment_amount,
            )

        #  create a transaction
        Transaction.objects.create(
            user=instance.share.owner,
            amount=instance.amount,
            transaction_type='withdrawal',
            date=timezone.now(),
            bank_account=instance.bank_account
        )
