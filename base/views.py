from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ReserveForm
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Room, Reserve

from django.core.mail import send_mail

# Home View
def home(request):
    context = {'user': request.user, 'reserve_id': None, 'room_id':None}  # Ensure reserve_id exists
    return render(request, 'base/home.html', context)


# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful')
            room_id = request.GET.get("room_id")  
            if room_id:
                return redirect('book', room_id=room.id)
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'base/login.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")  
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username:
            messages.error(request, "Username is required.")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login_view")

    return render(request, "base/register.html")

# Amenities View
def amenities(request):
    return render(request, 'base/Amenities.html')

@login_required(login_url='login_view')
def book(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == "POST":
        form = ReserveForm(request.POST)
        if form.is_valid():
            reserve = form.save(commit=False)
            reserve.user = request.user  
            reserve.room = room
            reserve.save()
            messages.success(request, f"Reservation for {reserve.name} has been submitted successfully!")
            return redirect('rates', reserve_id=reserve.id)  
        else:
            messages.error(request, "There was an error in your reservation form.")
    else:
        form = ReserveForm()

    return render(request, 'base/book.html', {'form': form})


def rates(request, reserve_id):
    if reserve_id is None:
        messages.error('please choose a room before you navigate to rates')
        return redirect('rooms')
    reserves = Reserve.objects.get(id=reserve_id)
    total_price = reserves.population * reserves.room.price
    return render(request, 'base/rates.html', {'reserves': reserves, 'total_price': total_price})


def rates(request, reserve_id=None):
    if reserve_id is None:
        messages.error(request, 'Please choose a room before navigating to rates.')
        return redirect('rooms')  
    reserves = get_object_or_404(Reserve, id=reserve_id)

    total_price = reserves.population * reserves.room.price if reserves.room else 0

    return render(request, 'base/rates.html', {'reserves': reserves, 'total_price': total_price})




# Contact View
def contact(request):
    return render(request, 'base/contact.html')

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login_view')



@csrf_exempt  # Disable CSRF for API calls (consider security in production)
def stk_push(request):
    if request.method == "POST":
        try:
            # Parse incoming JSON data from the frontend
            data = json.loads(request.body)
            phone = data.get("phone")
            amount = data.get("amount")

            if not phone or not amount:
                return JsonResponse({"success": False, "message": "Phone and Amount are required"}, status=400)

            # Flask API endpoint
            flask_url = "http://127.0.0.1:5001/stkpush"

            # Send request to Flask
            response = requests.post(flask_url, json={"phone": phone, "amount": amount})
            
            # Return Flask API response to Django frontend
            return JsonResponse(response.json(), status=response.status_code)

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"}, status=500)

    return JsonResponse({"success": False, "message": "Only POST requests allowed"}, status=405)


def message_mail(request):
    send_mail(
        subject='hello world',
        message='django smtp email',
        from_email='hello@demomailtrap.com',
        recipient_list=['geniusokwemba53@gmail.com']
    )
    messages.success(request, "Email sent succefully.")

def gallery(request):
    return render(request, 'base/gallery.html')

def rooms(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request, 'base/rooms.html', context)

def visit(request):
    return render(request, 'base/visit.html')