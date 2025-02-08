# railway/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User,Booking, Query ,Train # Correct the model name here
from .models import Train
User = get_user_model()
from django.contrib.auth import authenticate

from django import forms
from .models import Booking, Train

from django import forms
from .models import Booking, Train

from django import forms
from .models import Booking, Train

# Define gender choices above the BookingForm class
gender_choices = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]  # Gender options
from django import forms
from .models import Booking
from django.core.exceptions import ValidationError
from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from .models import Booking
from datetime import datetime
from django import forms
from .models import Booking
from datetime import datetime
from django import forms
from .models import Booking
from datetime import datetime

class BookingForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('PayPal', 'PayPal'),
        ('Bank Transfer', 'Bank Transfer'),
    ]

    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, initial='Credit Card')
    departure_time = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], required=True)
    arrival_time = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], required=True)

    class Meta:
        model = Booking
        fields = ['passenger_name', 'passenger_age', 'passenger_gender', 'passenger_type', 
                  'contact_number', 'email', 'train_number', 'train_name', 
                  'source', 'destination', 'departure_time', 'arrival_time', 
                  'travel_class','payment_method']
    
    
    def clean_departure_time(self):
        departure_time = self.cleaned_data.get('departure_time')
        if departure_time:
            # Extract only the time (without the date part)
            departure_time = departure_time.time()
        return departure_time
    
    def clean_arrival_time(self):
        arrival_time = self.cleaned_data.get('arrival_time')
        if arrival_time:
            # Extract only the time (without the date part)
            arrival_time = arrival_time.time()
        return arrival_time
    
from django import forms
from .models import Booking
from django.core.exceptions import ValidationError
from datetime import datetime



from django import forms

from django.contrib.auth.models import User  # Default User model
# railway/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# railway/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    email = forms.EmailField(required=True, help_text="Required. Provide a valid email address.")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

# railway/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EmailLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(username=email, password=password)  # Authenticate using email as username
        if not user:
            raise forms.ValidationError("Invalid email or password")
        return self.cleaned_data

# railway/forms.py
# railway/forms.py

from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid username or password")
        return self.cleaned_data

from django import forms
from django.contrib.auth import authenticate



'''
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean(self):
        email = self.cleaned_data.get('username')  # username field now holds email
        password = self.cleaned_data.get('password')
        
        if email and password:
            self.user_cache = authenticate(username=email, password=password)  # Adjusted for email as username
            if self.user_cache is None:
                raise forms.ValidationError("Invalid email or password.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
        
        return self.cleaned_data
'''

'''
class EmailLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise forms.ValidationError("Invalid password.")
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email.")

            cleaned_data['user'] = user
        return cleaned_data

    def get_user(self):
        return self.cleaned_data.get('user')

#class LoginForm(forms.Form):
 #   username = forms.CharField(max_length=150)
  #  password = forms.CharField(widget=forms.PasswordInput)
'''


from django import forms
from .models import Query

class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['user_email', 'subject', 'message']

    # Additional custom validation, if needed
    def clean_user_email(self):
        email = self.cleaned_data.get('user_email')
        if not email:
            raise forms.ValidationError("Please provide an email address.")
        return email

# forms.py
# forms.py

class TrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = ['train_number', 'source', 'destination', 'departure_time', 'arrival_time']
        widgets = {
            'departure_time': forms.TimeInput(attrs={'type': 'time'}),
            'arrival_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        
# forms.py

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'passenger_name', 'passenger_age', 'passenger_gender', 
                  'passenger_type', 'contact_number', 'email',
                  'train_number', 'train_name', 'source', 'destination', 
                  'departure_time', 'arrival_time', 'travel_class'
        ]
        widgets = {
            'date': forms.SelectDateWidget(),
            'travel_class': forms.RadioSelect()
        }
 