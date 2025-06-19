from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    send_email = forms.BooleanField(
        required=False,
        label="Send me a confirmation email"
    )
    confirmation_email = forms.EmailField(
        required=False,
        label="Your email address for confirmation",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email if you want a confirmation'})
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

    def clean(self):
        cleaned_data = super().clean()
        send_email = cleaned_data.get('send_email')
        confirmation_email = cleaned_data.get('confirmation_email')

        if send_email and not confirmation_email:
            self.add_error('confirmation_email', 'Please enter your email address to receive confirmation.')
