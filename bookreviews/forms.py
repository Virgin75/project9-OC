from django.forms import ModelForm
from django import forms
from bookreviews.models import Ticket, Review


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'descripton', 'image']


class ReviewForm(ModelForm):

    class Meta:
        CHOICES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]

        model = Review
        fields = ['rating', 'headline', 'body']
        widgets = {
            'rating': forms.RadioSelect(choices=CHOICES)
        }
