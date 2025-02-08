from django.db import models
from django.contrib.auth.models import User  # Use the default User model
from django.utils import timezone
import random
import string

def generate_reference_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

# Function to generate a unique reference number
def generate_reference_number():
    # Implement logic to generate a unique reference number
    return "UNIQUE_REF_12345"

from django.db import models
from django.contrib.auth.models import User
import uuid

# Function to generate a reference number for each booking
def generate_reference_number():
    return str(uuid.uuid4().hex[:8].upper())  # Using UUID for reference number generation
class Train(models.Model):
    train_number = models.CharField(max_length=10, unique=True)  # Ensuring unique train number
    train_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField(null=True, blank=True)  # Change to DateTimeField to include date and time
    arrival_time = models.TimeField(null=True, blank=True)  # Change to DateTimeField to include date and time
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.train_number} - {self.train_name} from {self.source} to {self.destination}"


class Booking(models.Model):
    
    train = models.ForeignKey(Train, on_delete=models.CASCADE)  # Removed default
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    reference_number = models.CharField(max_length=50, default=generate_reference_number, unique=True)
    booking_date = models.DateTimeField(auto_now_add=True)

    # Train information
    train_number = models.CharField(max_length=10)
    train_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField(null=True, blank=True)
    arrival_time = models.DateTimeField(null=True, blank=True)
    
    # Travel details
    travel_class = models.CharField(max_length=6, choices=[('AC', 'AC'), ('Non-AC', 'Non-AC')])
    seat_number = models.CharField(max_length=10, blank=True, null=True)
    number_of_tickets = models.PositiveIntegerField(default=1)
    # Fare details
    base_fare = models.DecimalField(max_digits=10, decimal_places=2)
    service_tax = models.DecimalField(max_digits=10, decimal_places=2)
    total_fare = models.DecimalField(max_digits=10, decimal_places=2)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    # Payment details
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    transaction_id = models.CharField(max_length=20, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')

    # Passenger contact details
    email = models.EmailField()
    passenger_name = models.CharField(max_length=100)
    passenger_age = models.IntegerField(null=True)
    passenger_gender = models.CharField(max_length=10)
    passenger_type = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)
    
    # Booking status
    STATUS_CHOICES = [('Active', 'Active'), ('Cancelled', 'Cancelled')]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def save(self, *args, **kwargs):
        if not self.seat_number:
            # Generate a random seat number between 1 and 100 for example
            self.seat_number = f"S{random.randint(1, 100)}"
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'booking_booking'

    def __str__(self):
        return f"{self.passenger_name} - {self.train_number}"



class Query(models.Model):
    user_email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Solved', 'Solved')], default='Pending')
    solved = models.BooleanField(default=False)  # New field to track solved status

    class Meta:
        db_table = 'railway_query'
    def __str__(self):
        return f"Query from {self.user_email} - {self.subject}"