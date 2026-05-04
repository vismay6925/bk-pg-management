from django.core.management.base import BaseCommand
from pgapp.models import Tenant


class Command(BaseCommand):
    help = "Reset all tenants payment status every month"

    def handle(self, *args, **kwargs):
        tenants = Tenant.objects.all()

        for tenant in tenants:
            tenant.is_paid = False
            tenant.save()

        print("All tenant payments reset to unpaid.")