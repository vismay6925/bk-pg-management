from django.core.management.base import BaseCommand
from pgapp.models import Tenant


class Command(BaseCommand):
    help = "Send payment reminders"

    def handle(self, *args, **kwargs):
        tenants = Tenant.objects.all()

        for tenant in tenants:
            status = tenant.reminder_status()

            if status in ["Send Once", "Send Daily"]:
                message = f"Reminder: {tenant.name}, please pay your rent."

                # 🔥 For now just print
                print(f"Sending to {tenant.phone}: {message}")