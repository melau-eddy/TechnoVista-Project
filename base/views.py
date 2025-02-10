from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ReserveForm
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Home View
def home(request):
    return render(request, 'base/home.html', {'user': request.user})

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('book')
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
def book(request):
    if request.method == "POST":
        form = ReserveForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user  # Associate the reservation with the logged-in user
            reservation.save()
            messages.success(request, f"Reservation for {reservation.name} has been submitted successfully!")
            return redirect('book')  # Redirect back to the booking page or another page
        else:
            messages.error(request, "There was an error in your reservation form.")
    else:
        form = ReserveForm()

    return render(request, 'base/book.html', {'form': form})


# Rates View
def rates(request):
    return render(request, 'base/rates.html')

# Contact View
def contact(request):
    return render(request, 'base/contact.html')

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login_view')


# timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

# def get_mpesa_token():
#     consumer_key = "UCOLz4IHesReIjmyWswYALA5UWAtlPzKfLZk6H9TSAY0bjIg"
#     consumer_secret = "ACbpFsQMikEdGwBIwQX7EglxHsBj26GJJmde42pvMzP2NIaYyHGcp5RK79OuHAMQ"
#     api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
#     try:
#         r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
#         r.raise_for_status()
#         response_data = r.json()
#         return response_data.get('access_token')
#     except requests.exceptions.RequestException as e:
#         return None



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
