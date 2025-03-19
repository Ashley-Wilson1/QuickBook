from django import forms
from .models import Room


# how the booking form will look
class AvailabilityForm(forms.Form):  
    room_number = forms.ChoiceField(choices=[],required=True)

    def __init__(self, *args, **kwargs):# grabs all rooms
        super().__init__(*args, **kwargs)
        self.fields['room_number'].choices = [(room.number, room.number) for room in Room.objects.all()]

    start_datetime = forms.DateTimeField(required=True,widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
        }))
    end_datetime = forms.DateTimeField(required=True,widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
        }))
    
    want_another_room = forms.BooleanField(required=False, initial=False, label="Allow automatic booking of another room if requested room is unavailable")

