from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        # Exclude 'user' because it's assigned in the view, not by the form
        fields = ['tool', 'date', 'start_time', 'end_time']
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
