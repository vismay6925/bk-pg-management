from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from datetime import date
import csv

from .models import Tenant, Bed, Room, Payment


# 🔥 LANDING PAGE
def home(request):
    return render(request, 'pgapp/home.html')


# 🔐 LOGIN VIEW
def login_view(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            error = "Invalid username or password"

    return render(request, 'pgapp/login.html', {'error': error})


# 🔓 LOGOUT VIEW
def logout_view(request):
    logout(request)
    return redirect('/login/')


# 🔥 DASHBOARD
@login_required(login_url='/login/')
def dashboard(request):

    total_tenants = Tenant.objects.count()
    total_beds = Bed.objects.count()
    occupied_beds = Tenant.objects.filter(bed__isnull=False).count()
    free_beds = total_beds - occupied_beds

    current_month = date.today().strftime("%B %Y")

    paid_tenants = Payment.objects.filter(
        month=current_month
    ).values_list('tenant_id', flat=True)

    pending_payments = Tenant.objects.exclude(
        id__in=paid_tenants
    ).count()

    context = {
        'total_tenants': total_tenants,
        'total_beds': total_beds,
        'occupied_beds': occupied_beds,
        'free_beds': free_beds,
        'pending_payments': pending_payments,
    }

    return render(request, 'pgapp/dashboard.html', context)


# 🔥 DOWNLOAD ALL DATA (NEW FEATURE)
@login_required(login_url='/login/')
def download_all_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pg_data.csv"'

    writer = csv.writer(response)

    # Header
    writer.writerow([
        'Tenant Name',
        'Phone',
        'Room',
        'Bed',
        'Rent',
        'Payment Status',
        'Month'
    ])

    current_month = date.today().strftime("%B %Y")

    tenants = Tenant.objects.select_related('bed__room').all()

    for tenant in tenants:
        bed = tenant.bed.number if tenant.bed else "-"
        room = tenant.bed.room.name if tenant.bed and tenant.bed.room else "-"

        paid = Payment.objects.filter(
            tenant=tenant,
            month=current_month
        ).exists()

        status = "Paid" if paid else "Pending"

        writer.writerow([
            tenant.name,
            tenant.phone,
            room,
            bed,
            tenant.rent,
            status,
            current_month
        ])

    return response


# 🔥 SIMPLE BED VIEW
@login_required(login_url='/login/')
def bed_view(request):
    beds = Bed.objects.all().order_by('number')

    data = []
    for bed in beds:
        tenant = getattr(bed, 'tenant', None)

        data.append({
            'number': bed.number,
            'status': 'occupied' if tenant else 'free',
            'tenant': tenant.name if tenant else None
        })

    return render(request, 'pgapp/beds.html', {'beds': data})


# 🔥 BED DASHBOARD
@login_required(login_url='/login/')
def bed_dashboard(request):
    rooms = Room.objects.all()

    room_data = []

    for room in rooms:
        beds = Bed.objects.filter(room=room).order_by('number')

        bed_list = []
        for bed in beds:
            tenant = getattr(bed, 'tenant', None)

            bed_list.append({
                'number': bed.number,
                'tenant': tenant.name if tenant else None,
                'occupied': bool(tenant)
            })

        room_data.append({
            'room': room.name,
            'beds': bed_list
        })

    return render(request, 'pgapp/bed_dashboard.html', {
        'room_data': room_data
    })