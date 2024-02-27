# Generated by Django 5.0.2 on 2024-02-25 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0002_loan_last_installment_amount_loan_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='installment',
            name='status',
        ),
        migrations.AddField(
            model_name='installment',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='installment',
            name='notes',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='installment',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='installment',
            name='paid_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='loan',
            name='checkout',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='loan',
            name='notes',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='loan',
            name='paid_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='installment',
            name='amount',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='loan',
            name='amount',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
