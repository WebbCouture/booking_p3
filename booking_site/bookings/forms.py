from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    send_email = forms.BooleanField(
        required=False,
        label="Send me a confirmation email"
    )

    class Meta:
        model = Booking
        fields = ['tool', 'date']  # Removed 'start_time' and 'end_time'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disable the tool field if pre-selected
        if self.initial.get('tool'):
            self.fields['tool'].disabled = True
