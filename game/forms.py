from django import forms
from game.models import Game


class CreateGameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ['name', 'gamer_count', 'steps_number', 'holding_cost', 'backorder_cost']
