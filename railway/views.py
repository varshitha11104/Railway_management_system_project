from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, BookingForm, QueryForm, EmailLoginForm
from .models import User, Train, Query
from django import forms
from .models import Query
from django.http import HttpResponse
# railway/views.py

from .forms import RegistrationForm, BookingForm, QueryForm  # Remove EmailLoginForm if not needed
# railway/views.py

from .forms import RegistrationForm, LoginForm  # Use RegistrationForm, not RegisterForm
# railway/views.py

from .forms import RegistrationForm, LoginForm  # Ensure 'RegistrationForm' is used instead of 'RegisterForm'


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages


# railway/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create the user but don't save it yet
            user = form.save(commit=False)
            # Set additional fields
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.email = form.cleaned_data.get("email")

            # Save the user
            user.save()

            # Set the backend manually if necessary
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            
            # Log the user in immediately after registration
            login(request, user)

            messages.success(request, "Registration successful!")
            return redirect("home")
    else:
        form = RegistrationForm()

    return render(request, "railway/register.html", {"form": form})





def login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)  # Use EmailLoginForm here
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home or dashboard
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = EmailLoginForm()

    return render(request, 'booking/profile.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')


def email_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Assuming you have a LoginForm
        if form.is_valid():
            # Extract email and password from form
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authenticate user using email (instead of username)
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # Log the user in if authentication is successful
                login(request, user, backend='railway.backends.EmailBackend')
                return redirect('home')  # Redirect to a success page
            else:
                # Return an error message if authentication fails
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()

    return render(request, 'railway/login.html', {'form': form})


def home(request):
    return render(request, 'railway/home.html')


from django.contrib.auth.decorators import login_required
from .models import Query
from .forms import QueryForm  # Ensure you have a form for Query model
@login_required
def raise_query(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Create a new Query object with the form data
        Query.objects.create(user_email=email, subject=subject, message=message)

        # After saving the query, redirect to the query success page
        return redirect('query_success')  # Corrected the redirect

    return render(request, 'railway/raise_query.html')

def query_success(request):
    return render(request, 'railway/query_successful.html')


def your_view(request):
    if request.method == 'POST':  # If the form was submitted
        form = YourForm(request.POST)
        if form.is_valid():       # Check if the data is valid
            form.save()           # Save it to the database
            return redirect('some-page')  # Redirect to another page if needed
    else:
        form = YourForm()         # If not submitted, show an empty form
    return render(request, 'your_template.html', {'form': form})

def save_data_view(request):
    if request.method == 'POST':
        new_entry = YourModel(field1='value1', field2='value2')
        new_entry.save()  # Manually save the data to the database
from django.shortcuts import render

# forms.py

class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['subject', 'message']

from django.db import transaction

@login_required
def submit_query(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                Query.objects.create(
                    subject=form.cleaned_data['subject'],
                    message=form.cleaned_data['message'],
                    user=request.user
                )
            return redirect('profile')
    else:
        form = QueryForm()
    return render(request, 'submit_query.html', {'form': form})
@login_required
def query_list(request):
    if request.user.is_authenticated:
        # Use the 'user_email' field instead of 'user'
        queries = Query.objects.filter(user_email=request.user.email)
        
        return render(request, 'railway/query_list.html', {'queries': queries})
    else:
        # If not authenticated, redirect or show an error
        return redirect('profile')
    
# booking/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Booking  # Make sure Booking model is imported
from django.urls import reverse


# booking/views.py

def home(request):
    return render(request, 'railway/home.html')
#@login_required  # Ensure the user is logged in to access this view


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.status = 'Cancelled'
        booking.save()
        return redirect('railway/booking_history')
    return render(request, 'railway/confirm_cancel.html', {'booking': booking})

# railway/views.py

from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from .models import Train


from django.shortcuts import render
from .models import Train
from django.utils.dateparse import parse_datetime
from django.shortcuts import render
from .models import Train
from django.utils.dateparse import parse_datetime
import logging
from django.shortcuts import render
from .models import Train
def search_trains(request):
    trains = None
    source = destination = ""

    if request.method == "POST":
        source = request.POST.get('source')
        destination = request.POST.get('destination')

        # Filter trains based on source and destination
        trains = Train.objects.all()

        if source:
            trains = trains.filter(source__icontains=source)
        if destination:
            trains = trains.filter(destination__icontains=destination)

        # Debugging print statements
        for train in trains:
            print(f"Train: {train.train_name}")
            print(f"Departure Time: {train.departure_time}")
            print(f"Arrival Time: {train.arrival_time}")
        
    return render(request, 'railway/search.html', {
        'trains': trains,
        'source': source,
        'destination': destination,
    })




# admin_panel/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from .models import Train
from .forms import TrainForm

# Utility function to check if a user is an admin
def is_admin(user):
    print("Checking if user is admin:", user.is_staff)  # Debugging line
    return user.is_staff
@login_required
def re_authenticate(request):
    if request.method == 'POST':
        username = request.user.username
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Successful authentication, log the user in again
            login(request, user)
            return redirect('/admin/')  # Redirect to the admin panel
        else:
            return render(request, 'admin_panel/re_authenticate.html', {'error': 'Invalid password.'})
    
    return render(request, 'admin_panel/re_authenticate.html')
#@login_required
#@user_passes_test(is_admin, login_url='/login/')
@login_required
@user_passes_test(is_admin)
def add_train(request):
    if request.method == 'POST':
        form = TrainForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administration_home')
    else:
        form = TrainForm()
    return render(request, 'admin_panel/add_train.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def update_train(request, train_id):
    train = get_object_or_404(Train, id=train_id)
    if request.method == 'POST':
        form = TrainForm(request.POST, instance=train)
        if form.is_valid():
            form.save()
            return redirect('administration_home')
    else:
        form = TrainForm(instance=train)
    return render(request, 'admin_panel/update_train.html', {'form': form})
@login_required
@user_passes_test(is_admin)
def list_trains(request):
    trains = Train.objects.all()
    return render(request, 'admin_panel/list_trains.html', {'trains': trains})




# views.py

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

def admin_home_page(request):
    return render(request, 'railway/admin_home_page.html')




def administration_login(request):
    return render(request, 'booking/administration_login.html')

def passenger_login(request):
    return render(request, 'booking/passenger_login.html')

def customer_support_login(request):
    return render(request, 'booking/support_login.html')

def profile(request):
    return render(request, 'booking/profile.html')

def administration_login(request):
    return render(request, 'booking/administration_login.html')

def passenger_login(request):
    return render(request, 'booking/passenger_login.html')

def customer_support_login(request):
    return render(request, 'booking/support_login.html')


from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def passenger_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Get the user associated with this email
        user = User.objects.filter(email=email).first()
        
        if user:
            # Authenticate using the username and password
            authenticated_user = authenticate(request, username=user.username, password=password)
            
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('home')  # Redirect to home page after login
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")

        return redirect('passenger_login')

    return render(request, 'booking/passenger_login.html')

# Support Login View
def support_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate the user with email and password
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Check if the user belongs to the 'Customer Support' group
            if user.groups.filter(name='Customer Support').exists():
                login(request, user)  # Log the user in
                return redirect('booking:support_home')  # Redirect to the support home page
            else:
                messages.error(request, "You do not have access to the Customer Support area.")
                return redirect('booking:support_login')  # Redirect back to login page
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('booking:support_login')  # Redirect back to login page

    return render(request, 'booking/support_login.html')
@login_required
def support_home(request):
    # Check if the logged-in user belongs to the 'Customer Support' group
    if request.user.groups.filter(name='Customer Support').exists():
        return render(request, 'booking/support_home.html')  # Render the support home page
    else:
        return redirect('support_login')  # Redirect to login page if the user
    
    
    
    from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def administration_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate the user with email
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Check if the user is in the 'Admin' group
            if user.groups.filter(name='Admin').exists():
                login(request, user)
                return redirect('admin_home_page')
            else:
                messages.error(request, "You do not have admin access.")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'booking/administration_login.html')

@csrf_protect
def customer_support_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate the user with email
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Check if the user is in the 'Admin' group
            if user.groups.filter(name='Admin').exists():
                login(request, user)
                return redirect('view_queries')
            else:
                messages.error(request, "You do not have admin access.")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'booking/customer_support_login.html')

def administration_home(request):
    # Check if the user has the admin group
    if request.user.groups.filter(name='Admin').exists():
        return render(request, 'booking/administration_home.html')  # Render the admin home page
    else:
        return redirect('booking/administration_login')
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')  # Redirect to the login page or any other page



from .forms import BookingForm
from .models import Booking
import random
import string
from django.shortcuts import render, redirect
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
import random
import string
# In your views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import random
import string
from .forms import BookingForm
from .models import Booking
import logging
import random
import string


# Configure logging
logger = logging.getLogger(__name__)


from decimal import Decimal


#@login_required
@login_required
def booking_view(request):
    trains = []  # Store available trains
    selected_train = None  # To hold the selected train if any
    email = request.user.email
    user_id=request.user.id
    if request.method == 'POST':
        passenger_name = request.POST.get('passenger_name')
        passenger_age = request.POST.get('passenger_age')
        passenger_gender = request.POST.get('passenger_gender')
        train_id = request.POST.get('train')
        number_of_tickets=request.POST.get('num_seats')
        travel_class=request.POST.get('ac_non_ac')

        if 'search_trains' in request.POST:  # Handle train search
            source = request.POST.get('source')
            destination = request.POST.get('destination')

            # Fetch trains matching source and destination
            if source and destination:
                trains = Train.objects.filter(source=source, destination=destination)
                if not trains:
                    messages.error(request, "No trains available for the selected route.")
            else:
                messages.error(request, "Both source and destination are required.")

        elif 'book_train' in request.POST:  # Handle train booking
            if not train_id:
                messages.error(request, "Please select a train to book.")
                return render(request, 'booking/booking_form.html', {'trains': trains})

            try:
                selected_train = Train.objects.get(id=train_id)

                # Generate booking details
                reference_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                seat_number = f"S{random.randint(1, 100)}"
                payment_amount = selected_train.ticket_price 
                # Calculate fares dynamically
                base_fare = 100  # Dynamic fare based on the selected train
                service_tax = base_fare * 0.1  # Example: 10% service tax
                total_fare = base_fare + service_tax

                # Create and save booking
                booking = Booking(
                    passenger_name= request.user.username
,
                    passenger_age=passenger_age,
                    passenger_gender=passenger_gender,
                    train_id=train_id,
                    train=selected_train,
                    payment_amount=(payment_amount *Decimal(number_of_tickets))+ Decimal(total_fare),
                    reference_number=reference_number,
                    seat_number=seat_number,
                    base_fare=base_fare,
                    service_tax=service_tax,
                    total_fare=total_fare,
                    email=email,
                    source=selected_train.source,
                    destination=selected_train.destination,
                    train_number=selected_train.train_number,
                    number_of_tickets =number_of_tickets,
                    travel_class=travel_class,
                    user_id=user_id
                    
                )
                booking.save()
                messages.success(request, f"Booking successful! Reference: {reference_number}")
                return redirect('payment_view', booking_id=booking.id)  # Redirect to payment page

            except Train.DoesNotExist:
                messages.error(request, "Selected train does not exist.")

    return render(request, 'booking/booking_form.html', {
        'trains': trains,
        'selected_train': selected_train,
    })

@login_required




def payment_view(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return HttpResponse("Booking not found", status=404)

    if request.method == 'POST':
        # Process payment (this is just an example)
        # You can integrate a real payment gateway here
        payment_method = request.POST.get('payment_method')

        # Ensure payment method is provided
        if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return render(request, 'payment_form.html', {'booking': booking})
        
        # Update the booking with the payment method
        booking.payment_method = payment_method
        booking.payment_status = 'Paid'  # Mark the payment status as 'Paid'
        booking.status = 'Active'  # Update the booking status (could be 'Active' or another status)
        booking.save()
        
        # Redirect to payment success page
        return redirect('payment_success', booking_id=booking.id)

    return render(request, 'booking/payment_form.html', {'booking': booking})

from django.shortcuts import render
from .models import Train  # assuming you have a Train model

def find_trains(request):
    trains = Train.objects.all()  # Get available trains
    
    if request.method == 'POST':
        if 'search_trains' in request.POST:
            source = request.POST['source']
            destination = request.POST['destination']
            trains = Train.objects.filter(source=source, destination=destination)

        elif 'book_train' in request.POST:
            train_id = request.POST['train']
            passenger_name = request.POST['passenger_name']
            passenger_age = request.POST['passenger_age']
            passenger_gender = request.POST['passenger_gender']

            selected_train = Train.objects.get(id=train_id)
            booking = Booking.objects.create(
                train=selected_train,
                passenger_name=passenger_name,
                passenger_age=passenger_age,
                passenger_gender=passenger_gender
            )
            # Optionally, display success message or redirect
            messages.success(request, "Booking successfully made!")
            return render(request, 'search.html', {'trains': trains, 'source': source, 'destination': destination})

    return render(request, 'search.html', {'trains': trains})


# Define your fare calculation functions
def calculate_base_fare(booking):
    # Example: A base fare calculation based on train number or class
    return 1500  # Just an example, can be based on various factors

def calculate_service_tax(booking):
    # Example: Service tax is 5% of the base fare
    return booking.base_fare * 0.05
def booking_success(request):
    return render(request, 'railway/success.html')

'''#@login_required
def user_booking_history(request):
    """Fetch and display the booking history of the logged-in user."""
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/booking_history.html', {'bookings': bookings})
'''
@login_required
def user_booking_history(request):
    """Fetch and display the booking history of the logged-in user."""
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(email=request.user.email)
        return render(request, 'booking/booking_history.html', {'bookings': bookings})
    else:
        message = "Please log in to view your booking history."
        return render(request, 'booking/booking_history.html', {'message': message})

@login_required
def booking_details(request, booking_id):
    """Display the details of a specific booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking/booking_details.html', {'booking': booking})




@login_required
def cancel_booking(request, booking_id):
    print(f"Booking ID: {booking_id}")
    print(f"Logged-in User: {request.user} (ID: {request.user.id})")

    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        booking.status = 'Cancelled'
        booking.save()
        return redirect('booking_history')

    return render(request, 'booking/confirm_cancel.html', {'booking': booking})


def all_bookings(request):
    bookings = Booking.objects.select_related('user').all() 
    print("Booking count:", bookings.count())  # Debugging line
    for booking in bookings:
        print(booking)  # Print each booking to see the data
    return render(request, 'booking/all_bookings.html', {'bookings': bookings})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Booking


from django.shortcuts import render, redirect, get_object_or_404
from railway.models import Query

def view_queries(request):
    queries = Query.objects.all()
    return render(request, 'railway/view_queries.html', {'queries': queries})

def solve_query(request, query_id):
    query = get_object_or_404(Query, id=query_id)
    query.status = 'Solved'
    query.solved = True
    query.save()
    return redirect('view_queries')  # Redirect back to the queries page
from .models import Query  # Assuming you have a Query model to store passenger queries

@login_required
def user_queries(request):
    """Fetch and display the queries raised by the logged-in user."""
    if request.user.is_authenticated:
        # Filter queries based on the logged-in user's email
        queries = Query.objects.filter(user_email=request.user.email)

        return render(request, 'queries/user_queries.html', {'queries': queries})
    else:
        # If the user is not authenticated
        message = "Please log in to view your queries."
        return render(request, 'queries/user_queries.html', {'message': message})
    



@login_required
def payment_success(request, booking_id):
    try:
        # Fetch the booking details using the booking_id
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return HttpResponse("Booking not found", status=404)

    # Pass the booking details to the template
    return render(request, 'booking/booking_ticket_details.html', {'booking': booking})
@login_required
def payment_view(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return HttpResponse("Booking not found", status=404)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return render(request, 'payment_form.html', {'booking': booking})

        booking.payment_method = payment_method
        booking.payment_status = 'Paid'
        booking.status = 'Active'  # Change status as required (Active/Confirmed)
        booking.save()
        return redirect('payment_success', booking_id=booking.id)

    return render(request, 'booking/payment_form.html', {'booking': booking})


def payment_process(request):
    """Handle the payment for the booking"""
    if request.method == 'POST':
        # Get the booking and payment method from the form
        booking_id = request.POST.get('booking_id')
        payment_method = request.POST.get('payment_method')

        # Ensure booking_id and payment_method are provided
        if not booking_id or not payment_method:
            return HttpResponse("Missing payment details", status=400)

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return HttpResponse("Booking not found", status=404)

        # Simulate payment processing (you can integrate with a real payment gateway here)
        booking.payment_status = 'Paid'
        booking.payment_method = payment_method
        booking.save()

        # After successful payment, redirect to a payment success page
        return redirect('payment_success', booking_id=booking.id)

    else:
        return redirect('home')  # Redirect to home if form is not valid


def ticket_view(request, reference_number):
    try:
        # Fetch the booking using the reference number
        booking = Booking.objects.get(reference_number=reference_number)
    except Booking.DoesNotExist:
        return HttpResponse("Booking not found", status=404)

    return render(request, 'ticket.html', {'booking': booking})

