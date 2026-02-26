from django.contrib import admin
from .models import AdminUser,UserProfile,Vehicle,Service,Booking,Mechanic,ServiceAssignment


# Register your models here.
@admin.register(AdminUser)
class AdminUser(admin.ModelAdmin):
    list_display=('email','password')

@admin.register(UserProfile)
class UserprofileAdmin(admin.ModelAdmin):
    list_display=('user_id','name','email','phone','password')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display=('user', 'vehicle_number','brand','model','year')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display=('user','name','description','price','duration')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display=('user','vehicle_number','service','booking_date','status')

@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display=('name','phone')

@admin.register(ServiceAssignment)
class ServiceAssignmentAdmin(admin.ModelAdmin):
    list_display=('booking','mechanic')