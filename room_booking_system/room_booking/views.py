from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, FormView,DetailView
from .models import Room, RoomBooking

# def dashboard(request):
#     return render(request, 'dashboard.html', {})

class BookingList(ListView):
    model=RoomBooking
    template_name = 'dashboard.html'
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff: #super user also staff
            booking_list= RoomBooking.objects.all()
            return booking_list
        else:
            booking_list = RoomBooking.objects.filter(user=self.request.user) # only returns users bookings
            return booking_list

class BookingDetailView(DetailView):
    model = RoomBooking
    template_name = "booking_details.html"

def cancel_booking(request, booking_id):
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