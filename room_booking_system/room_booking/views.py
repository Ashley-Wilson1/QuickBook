from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, FormView,DetailView,CreateView
from .models import Room, RoomBooking
from .forms import AvailabilityForm
from django.contrib import messages
# def dashboard(request):
#     return render(request, 'dashboard.html', {})

class BookingList(ListView):
    model=RoomBooking
    template_name = 'dashboard.html'
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff: #super user also staff
            booking_list= RoomBooking.objects.all()
        else:
            booking_list = RoomBooking.objects.filter(user=self.request.user) # only returns users bookings
            
        # Consume messages so they don't appear again
        list(messages.get_messages(self.request))
        return booking_list

class BookingDetailView(DetailView):
    model = RoomBooking
    template_name = "booking_details.html"

def CancelBooking(request, booking_id):
    if request.method == "POST":
        if request.user.is_superuser:
            # Superuser can delete any booking
            booking = get_object_or_404(RoomBooking, id=booking_id)
        else:
            # Regular users can only delete their own bookings
            booking = get_object_or_404(RoomBooking, id=booking_id, user=request.user)

        booking.delete()
        return redirect('dashboard')  # Redirect to the booking list page

    return redirect('dashboard')  # Redirect if accessed without POST



class CreateBooking(FormView):
    form_class = AvailabilityForm
    template_name = 'create_booking.html'

    def form_valid(self, form):
        data = form.cleaned_data
        room_number = data['room_number']
        requested_room = Room.objects.get(number=room_number)  # Get the selected room

        try:
            # Try to create the booking
            booking = RoomBooking.objects.create(
                user=self.request.user,
                room=requested_room,
                start_datetime=data['start_datetime'],
                end_datetime=data['end_datetime']
            )
            messages.success(self.request, "Booking created successfully!")
            return redirect('dashboard')

        except ValidationError as e:
            messages.error(self.request, e.messages[0])# Show error message to user
            return self.form_invalid(form)  # Re-render form with errors
