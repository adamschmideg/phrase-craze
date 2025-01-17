from django import forms
from quiz import models

class StatusForm(forms.ModelForm):
    class Meta:
        model = models.Status
        fields = ['question_difficulty', 'answer_difficulty', 'matches_played', 'matches_won', 'matches_per_round']
