from django.contrib import admin
from django.db import models
from django.http import HttpResponse
from django import forms
import csv
from datetime import date

from .models import Tenant, Bed, Room, ActivityLog, Payment


# 🔥 PAYMENT FORM (AUTO MONTH IN UI)
class PaymentAdminForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 👉 Auto-fill month in form (before save)
        if not self.instance.pk:
            today = date.today()
            self.fields['month'].initial = today.strftime("%B %Y")


# 🔥 Tenant Admin
class TenantAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'phone', 'bed', 'rent', 'joining_date',
        'id_proof_type', 'payment_status'
    )
    search_fields = ('name', 'phone')
    list_filter = ('joining_date',)

    # 🔥 UPDATED PAYMENT STATUS (AUTO MONTH LOGIC)
    def payment_status(self, obj):
        return obj.current_month_status()

    payment_status.short_description = "Payment Status"

    # 🔥 Bed filtering (safe)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "bed":

            if request.path.endswith('/add/'):
                kwargs["queryset"] = Bed.objects.filter(tenant__isnull=True)

            else:
                obj_id = request.resolver_match.kwargs.get('object_id')

                if obj_id:
                    try:
                        tenant = Tenant.objects.get(pk=obj_id)
                        kwargs["queryset"] = Bed.objects.filter(
                            models.Q(tenant__isnull=True) |
                            models.Q(id=tenant.bed_id)
                        )
                    except Tenant.DoesNotExist:
                        kwargs["queryset"] = Bed.objects.filter(tenant__isnull=True)
                else:
                    kwargs["queryset"] = Bed.objects.filter(tenant__isnull=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# 🔥 Bed Admin
class BedAdmin(admin.ModelAdmin):
    list_display = ('number', 'room', 'occupied_status', 'tenant_name')

    def occupied_status(self, obj):
        if hasattr(obj, 'tenant'):
            return "🔴 Occupied"
        return "🟢 Available"

    occupied_status.short_description = "Status"

    def tenant_name(self, obj):
        tenant = getattr(obj, 'tenant', None)
        return tenant.name if tenant else "-"

    tenant_name.short_description = "Tenant"


# 🔥 Room Admin
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')


# 🔥 Activity Log Admin
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('tenant_name', 'bed_number', 'action', 'timestamp')
    search_fields = ('tenant_name', 'bed_number')
    list_filter = ('action',)
    actions = ['export_csv']

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="activity_log.csv"'

        writer = csv.writer(response)
        writer.writerow(['Tenant Name', 'Bed', 'Action', 'Date'])

        for log in queryset:
            writer.writerow([
                log.tenant_name,
                log.bed_number,
                log.action,
                log.timestamp
            ])

        return response

    export_csv.short_description = "Download selected logs as CSV"


# 🔥 Payment Admin
class PaymentAdmin(admin.ModelAdmin):
    form = PaymentAdminForm

    list_display = ('tenant', 'amount', 'month', 'date')
    search_fields = ('tenant__name', 'month')
    list_filter = ('month',)


# 🔥 REGISTER
admin.site.register(Tenant, TenantAdmin)
admin.site.register(Bed, BedAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(ActivityLog, ActivityLogAdmin)
admin.site.register(Payment, PaymentAdmin)