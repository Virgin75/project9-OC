from django.forms import ModelForm
from bookreviews.models import Ticket


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'descripton', 'image']
