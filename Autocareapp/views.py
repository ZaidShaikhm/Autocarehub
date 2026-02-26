from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

import random
import string

from .models import AdminUser, UserProfile, Vehicle, Service_status, Booking, Service

# Utility Functions
def generate_user_id():
    """Generate a random user ID of 8 characters."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Index Page
def index(request):
    return render(request, 'Autocareapp/index.html')

# Admin Authentication
def adminlogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            adminprofileobj = AdminUser.objects.get(email=email, password=password)
            request.session['adminemail'] = email
            request.session['adminpassword'] = password
            request.session['adminloggedin'] = True
            return redirect("adminhome")
        except AdminUser.DoesNotExist:
            messages.error(request, "Invalid email or password")
    return render(request, 'Autocareapp/adminlogin.html')

def adminhome(request):
    if not request.session.get("adminloggedin"):
        return redirect("adminlogin")
    return render(request, "Autocareapp/adminhome.html")

def adminlogout(request):
    request.session.flush()
    messages.success(request, "You have logged out, login again")
    return redirect("adminlogin")

def adminchangepassword(request):
    if not request.session.get("adminloggedin"):
        return redirect("adminlogin")
    if request.method == "POST":
        email = request.session.get("adminemail")
        currentpassword = request.POST["currentpassword"]
        newpassword = request.POST["newpassword"]
        try:
            adminobj = AdminUser.objects.get(email=email)
            if currentpassword == request.session.get("adminpassword"):
                adminobj.password = newpassword
                adminobj.save()
                messages.success(request, "Password changed successfully!")
                return redirect("adminlogin")
            else:
                messages.error(request, "Current password is invalid.")
        except AdminUser.DoesNotExist:
            messages.error(request, "This admin does not exist.")
    return render(request, "Autocareapp/adminchangepassword.html")

# User Authentication
def usersignup(request): 
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        # Check if email or phone already exists
        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, "Email ID already exists. Please use a different email.")
            return render(request, "Autocareapp/usersignup.html")

        if UserProfile.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists. Please use a different number.")
            return render(request, "Autocareapp/usersignup.html")

        # Generate a new user_id (auto-increment style)
        last_user = UserProfile.objects.order_by('-id').first()
        if last_user and last_user.user_id.isdigit():
            user_id = str(int(last_user.user_id) + 1)
        else:
            user_id = "1"

        # Create the user
        UserProfile.objects.create(
            user_id=user_id,
            name=name,
            email=email,
            phone=phone,
            password=password
        )

        messages.success(request, "Signup successful! Please log in.")
        return redirect('userlogin')

    return render(request, "Autocareapp/usersignup.html")
def userlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = UserProfile.objects.get(email=email, password=password)
            request.session['userloggedin'] = True
            request.session['user_id'] = user.user_id
            return redirect('userhomepage')
        except UserProfile.DoesNotExist:
            messages.error(request, "Invalid credentials")
    return render(request, 'autocareapp/userlogin.html')

def userhomepage(request):
    if not request.session.get('userloggedin'):
        return redirect('userlogin')
    name = request.session.get('useremail', 'User')
    return render(request, 'Autocareapp/userhomepage.html', {'name': name})

def userlogout(request):
    if request.session.get('userloggedin'):
        request.session.flush()
        messages.success(request, "You have successfully logged out.")
    return redirect('userlogin')

from .forms import VehicleForm


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Vehicle

def my_vehicle(request):
    if not request.session.get('userloggedin'):
        return redirect('userlogin')

    user_id = request.session.get('user_id')
    try:
        user = UserProfile.objects.get(user_id=user_id)  # Use user_id field, not pk
    except UserProfile.DoesNotExist:
        return redirect('userlogin')

    vehicles = Vehicle.objects.filter(user=user)  # This is correct

    return render(request, 'autocareapp/my_vehicle.html', {'vehicles': vehicles})

from django.contrib import messages

from django.contrib import messages

def ad_vehicle(request):
    if not request.session.get('userloggedin'):
        return redirect('userlogin')

    user_id = request.session.get('user_id')
    try:
        user = UserProfile.objects.get(user_id=user_id)
    except UserProfile.DoesNotExist:
        return redirect('userlogin')

    if request.method == 'POST':
        brand = request.POST.get('brand')
        brand_other = request.POST.get('brand_other')
        model = request.POST.get('model')
        model_other = request.POST.get('model_other')
        year = request.POST.get('year')
        vehicle_number = request.POST.get('vehicle_number')

        final_brand = brand_other if brand == 'Other' else brand
        final_model = model_other if model == 'Other' else model

        # Check for duplicate vehicle_number
        if Vehicle.objects.filter(vehicle_number=vehicle_number).exists():
            messages.error(request, "Vehicle number already exists!")
            return render(request, 'autocareapp/ad_vehicle.html')

        Vehicle.objects.create(
            user=user,  # Associate vehicle with the logged-in user
            brand=final_brand,
            model=final_model,
            year=year,
            vehicle_number=vehicle_number
        )
        messages.success(request, "Vehicle added successfully!")
        return redirect('my_vehicle')

    return render(request, 'autocareapp/ad_vehicle.html')

def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        brand = request.POST.get('brand')
        brand_other = request.POST.get('brand_other')
        model = request.POST.get('model')
        model_other = request.POST.get('model_other')
        year = request.POST.get('year')
        vehicle_number = request.POST.get('vehicle_number')

        vehicle.brand = brand_other if brand == 'Other' else brand
        vehicle.model = model_other if model == 'Other' else model
        vehicle.year = year
        vehicle.vehicle_number = vehicle_number
        vehicle.save()
        messages.success(request, "Vehicle updated successfully!")
        return redirect('my_vehicle')

    return render(request, 'autocareapp/edit_vehicle.html', {'vehicle': vehicle})

def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, "Vehicle deleted successfully!")
        return redirect('my_vehicle')
    return render(request, 'autocareapp/delete_vehicle_confirm.html', {'vehicle': vehicle})
# Service Status

from django.views.decorators.csrf import csrf_exempt
from django.utils.dateformat import DateFormat

def service_status_page(request):
    return render(request, 'autocareapp/service_status_page.html')

@csrf_exempt
def service_status(request):
    vehicle_number = request.GET.get('vehicle_number', '').strip().upper()
    try:
        vehicle = Vehicle.objects.get(vehicle_number=vehicle_number)
        bookings = Booking.objects.filter(vehicle_number=vehicle).order_by('-booking_date')
        services = []
        for booking in bookings:
            services.append({
                "service_type": str(booking.service),
                "description": getattr(booking.service, 'description', ''),  # If your Service model has description
                "amount": getattr(booking.service, 'amount', ''),            # If your Service model has amount
                "status": booking.status,
                "date": DateFormat(booking.booking_date).format('Y-m-d'),
            })
        return JsonResponse({"success": True, "services": services})
    except Vehicle.DoesNotExist:
        return JsonResponse({"success": False, "message": "No records found for this vehicle."})
    

from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service

def services(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        duration_str = request.POST.get('duration')  # expected format: hh:mm:ss

        try:
            # Parse duration string into timedelta
            h, m, s = map(int, duration_str.split(':'))
            duration = timedelta(hours=h, minutes=m, seconds=s)

            # Create and save new Service instance
            service = Service.objects.create(
                name=name,
                description=description,
                price=price,
                duration=duration
            )
            messages.success(request, "Service added successfully!")
            return redirect('services')

        except ValueError:
            messages.error(request, "Invalid duration format. Use hh:mm:ss.")
        except Exception as e:
            messages.error(request, f"Error adding service: {str(e)}")

    services = Service.objects.all()
    return render(request, 'Autocareapp/services.html', {'services': services})

def managebookings(request):
    bookings = Booking.objects.all()
    return render(request, 'Autocareapp/managebookings.html', {'bookings': bookings})




def about(request):
    return render(request, 'Autocareapp/about.html')


def adminvehicle(request):
    vehicles = Vehicle.objects.all().order_by('-id')  # You can add filters as needed
    return render(request, 'autocareapp/adminvehicle.html', {'vehicles': vehicles})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service, Vehicle, Booking, UserProfile

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service, Vehicle, Booking, UserProfile

def book_service(request):
    if not request.session.get('userloggedin'):
        return redirect('userlogin')
    user_id = request.session.get('user_id')
    try:
        user = UserProfile.objects.get(user_id=user_id)
    except UserProfile.DoesNotExist:
        return redirect('userlogin')

    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        vehicle_id = request.POST.get('vehicle_id')
        vehicle_number = request.POST.get('vehicle_number')
        brand = request.POST.get('brand')
        booking_date = request.POST.get('booking_date')
        brand_other = request.POST.get('brand_other')
        model = request.POST.get('model')
        model_other = request.POST.get('model_other')

        final_brand = brand_other if brand == 'Other' and brand_other else brand
        final_model = model_other if model == 'Other' and model_other else model

        try:
            service = Service.objects.get(id=service_id)
            if vehicle_id == "add_new":
                vehicle = Vehicle.objects.create(
                    user=user,
                    brand=final_brand,
                    model=final_model,
                    vehicle=vehicle_number
                )
            else:
                vehicle = Vehicle.objects.get(id=vehicle_id, user=user)

            Booking.objects.create(
                user=user,
                service=service,
                vehicle_number=vehicle,
                amount=service.amount,
                booking_date=booking_date
            )

            messages.success(request, "Service booked successfully!")
            return redirect('book_service')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    services = Service.objects.all()
    vehicles = Vehicle.objects.filter(user=user)
    return render(request, 'autocareapp/book_service.html', {
        'services': services,
        'vehicles': vehicles
    })



def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Accepted'
    booking.save()
    messages.success(request, "Booking accepted!")
    return redirect('managebookings')

def inprogress_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'In Progress'
    booking.save()
    messages.success(request, "Booking marked as In Progress!")
    return redirect('managebookings')

def complete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Completed'
    booking.save()
    messages.success(request, "Booking marked as Completed!")
    return redirect('managebookings')

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Cancelled'
    booking.save()
    messages.success(request, "Booking cancelled!")
    return redirect('managebookings')


from django.shortcuts import render
from datetime import datetime
def land(request):
    return render(request, 'Autocareapp/land.html')
  # or 'autocareapp/land.html' if your folder is lowercase

def abouut(request):
    return render(request, 'Autocareapp/abouut.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = UserProfile.objects.get(email=email)
            messages.success(request, f'Account found for {user.name}. Please contact admin to reset your password.')
            return redirect('userlogin')  # Or send reset link via email if implemented
        except UserProfile.DoesNotExist:
            messages.error(request, 'No user found with this email. Please create a new account.')
            return redirect('usersignup')

    return render(request, 'autocareapp/forgot_password.html')