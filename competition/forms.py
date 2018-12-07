from django import forms

from .models import Competition, Match, Participant


class CompetitionImportForm(forms.Form):
    competition = forms.ModelChoiceField(Competition.objects.all(), widget=forms.HiddenInput)
    participant_list = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(CompetitionImportForm, self).__init__(*args, **kwargs)

        self.fields['participant_list'].widget.attrs.update({'class': 'form-control'})

    def clean_participant_list(self):
        participant_list = self.cleaned_data['participant_list']

        participant_list = participant_list.split('\n')

        return participant_list

    def save(self):
        competition = self.cleaned_data['competition']
        participant_list = self.cleaned_data['participant_list']

        counter = 0

        for participant in participant_list:
            Participant.objects.create(name=participant, competition=competition)
            counter += 1

        return counter

class CompetitionSubmitForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['winner', 'loser', 'competition']

    def __init__(self, *args, **kwargs):
        super(CompetitionSubmitForm, self).__init__(*args, **kwargs)

        self.fields['competition'].widget = forms.HiddenInput()
        self.fields['winner'].widget.attrs.update({'class': 'form-control'})
        self.fields['loser'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super(CompetitionSubmitForm, self).clean()

        winner = cleaned_data['winner']
        loser = cleaned_data['loser']

        if winner == loser:
            raise forms.ValidationError('Výherca je tá istá osoba ako porazený')

        return cleaned_data
