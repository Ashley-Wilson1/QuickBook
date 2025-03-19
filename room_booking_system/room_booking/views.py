from django.shortcuts import render
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