from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
# Create your models here.


class User(AbstractUser):
    phone = models.CharField(_('Phone'), max_length=12, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Share(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.IntegerField()
    asset = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    # Add any other fields relevant to shares

    def __str__(self):
        return f'{self.owner.__str__()} | سهم {self.order}'

    def update_asset(self):
        # Assuming a fixed monthly addition to the asset
        # You can modify this logic as needed
        monthly_addition = 1000  # Example monthly addition amount
        self.asset += monthly_addition
        self.save()

    @classmethod
    def update_assets(cls):
        shares = cls.objects.all()
        for share in shares:
            share.update_asset()