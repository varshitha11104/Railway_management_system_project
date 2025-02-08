from django.contrib import admin
from .models import Train,Booking, Query, User
# Correct import in railway/admin.py
from .models import Booking  # Replace 'RailwayBooking' with your actual model's name

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

# Unregister the existing User model to avoid duplicates
#admin.site.register(User)

class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'reference_number',
        'train_number',  # Corresponds to the train's number
        'departure_time',  # Use departure time as journey-related field
        'seat_number',
        'total_fare',  # Total fare for the booking
        'payment_status',  # Display payment status
        'status',  # Active or Cancelled status
    )
    list_filter = (
        'train_number',  # Filter based on train number
        'travel_class',  # Filter based on class (AC, Non-AC)
        'payment_status',  # Filter based on payment status
        'status',  # Filter by Active/Cancelled status
    )

#admin.site.register(Booking, BookingAdmin)
# Register models to the admin site
admin.site.register(Train)  # Register Train model
admin.site.register(Booking, BookingAdmin)  # Register Booking model with the custom admin
admin.site.register(Query)  # Register Query model
class QueryAdmin(admin.ModelAdmin):
    #list_display = ('id', 'email', 'subject', 'message', 'status')  # Columns to display
    #list_filter = ('status',)  # Filter queries by their status
    #search_fields = ('email', 'subject')  # Allow search by email or subject
    list_display = ('status', 'user_email', 'subject', 'created_at')  # Status first, followed by email, subject, and created_at
    list_filter = ('status',)  # Option to filter by status (Pending/Resolved)
    search_fields = ('user_email', 'subject', 'message')  # Search queries by email, subject, or message

    # This adds an action to mark queries as resolved
    actions = ['mark_as_resolved']
    
    # Define the action to mark queries as resolved
    def mark_as_resolved(self, request, queryset):
        rows_updated = queryset.update(status='Resolved')
        if rows_updated == 1:
            message_bit = "1 query was"
        else:
            message_bit = f"{rows_updated} queries were"
        self.message_user(request, f"{message_bit} successfully marked as resolved.")
    
    mark_as_resolved.short_description = "Mark selected queries as resolved"

# Register the Query model with the custom admin configuration if it hasn't been registered already
if not admin.site.is_registered(Query):
    admin.site.register(Query, QueryAdmin)

