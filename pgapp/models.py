from django.db import models
from django.utils import timezone


# 🔥 Room Model
class Room(models.Model):
    name = models.CharField(max_length=20)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


# 🔥 Bed Model (✅ FIXED HERE)
class Bed(models.Model):
    number = models.CharField(max_length=10, unique=True)   # ✅ CHANGED
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        room_name = self.room.name if self.room else "No Room"
        return f"Bed {self.number} ({room_name})"


# 🔥 Tenant Model
class Tenant(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    bed = models.OneToOneField(Bed, on_delete=models.SET_NULL, null=True)

    rent = models.IntegerField()
    joining_date = models.DateField()

    # ID Proof
    id_proof_type = models.CharField(max_length=20, default='AADHAR')
    id_proof_file = models.FileField(upload_to='id_proofs/', null=True, blank=True)

    # Payment flag
    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 🔥 Due date
    def due_date(self):
        from datetime import timedelta
        return self.joining_date + timedelta(days=30)

    # 🔥 SMART STATUS
    def current_month_status(self):
        from datetime import date

        current_month = date.today().strftime("%B %Y")

        if Payment.objects.filter(tenant_id=self.pk, month=current_month).exists():
            return "Paid"

        if date.today() > self.due_date():
            return "Overdue"

        if date.today() == self.due_date():
            return "Due Today"

        return "Pending"

    def __str__(self):
        return self.name if self.name else "No Name"

    # 🔥 SAVE
    def save(self, *args, **kwargs):
        from datetime import date

        is_new = self.pk is None
        previous_paid = False

        if not is_new:
            try:
                previous = Tenant.objects.get(pk=self.pk)
                previous_paid = previous.is_paid
            except Tenant.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        # 🔥 Activity Log
        if is_new:
            ActivityLog.objects.create(
                tenant_name=self.name,
                bed_number=str(self.bed.number) if self.bed else "None",
                action="Added"
            )

        # 🔥 Auto Payment Entry
        if self.is_paid and not previous_paid:
            current_month = date.today().strftime("%B %Y")

            if not Payment.objects.filter(
                tenant_id=self.pk,
                month=current_month
            ).exists():
                Payment.objects.create(
                    tenant=self,
                    amount=self.rent,
                    date=date.today(),
                    month=current_month
                )

    # 🔥 DELETE
    def delete(self, *args, **kwargs):
        ActivityLog.objects.create(
            tenant_name=self.name,
            bed_number=str(self.bed.number) if self.bed else "None",
            action="Deleted"
        )
        super().delete(*args, **kwargs)


# 🔥 Activity Log
class ActivityLog(models.Model):
    tenant_name = models.CharField(max_length=100)
    bed_number = models.CharField(max_length=10)
    action = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tenant_name} - {self.action}"


# 🔥 Payment Model
class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount = models.IntegerField()

    date = models.DateField(default=timezone.now)
    month = models.CharField(max_length=20, blank=True)

    def __str__(self):
        tenant_name = self.tenant.name if self.tenant else "Unknown"
        return f"{tenant_name} - {self.month}"

    def save(self, *args, **kwargs):
        # 🔥 Auto-fill month
        if not self.month:
            self.month = self.date.strftime("%B %Y")

        super().save(*args, **kwargs)

        # 🔥 Sync payment flag
        if self.tenant_id:
            Tenant.objects.filter(pk=self.tenant_id).update(is_paid=True)