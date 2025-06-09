from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    send_email = forms.BooleanField(
        required=False,
        label="Send me a confirmation email"
    )

    class Meta:
        model = Booking
        fields = ['tool', 'date', 'start_time', 'end_time']  # 'send_email' is not part of the model
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disable the tool field if a tool is preselected (e.g., from tool_id in URL)
        if self.initial.get('tool'):
            self.fields['tool'].disabled = True
