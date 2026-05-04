from django.contrib import admin
from django.urls import path
from pgapp import views

urlpatterns = [
    # 🔧 Admin
    path('admin/', admin.site.urls),

    # 🔥 Landing Page
    path('', views.home, name='home'),

    # 🔐 Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 🏠 Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # 🛏 Bed Occupancy
    path('beds/', views.bed_dashboard, name='bed_dashboard'),

    # ⬇ Download All Data (NEW)
    path('download/', views.download_all_data, name='download'),
]