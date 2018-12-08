from django import forms

from .models import Competition, Match, Participant


class CompetitionImportForm(forms.Form):
    competition = forms.ModelChoiceField(Competition.objects.all(), widget=forms.HiddenInput)
    participant_list = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(CompetitionImportForm, self).__init__(*args, **kwargs)

        self.fields['participant_list'].widget.attrs.update({'class': 'form-control'})

    def clean_participant_list(self):
        competition = self.cleaned_data['competition']
        participant_string = self.cleaned_data['participant_list']

        participant_list = list(filter(lambda p: len(p) > 0, participant_string.splitlines()))

        for participant in participant_list:
            if Participant.objects.filter(competition=competition, name=participant).exists():
                raise forms.ValidationError('Účastník {} už existuje!'.format(participant))

        return participant_list

    def save(self):
        competition = self.cleaned_data['competition']
        participant_list = self.cleaned_data['participant_list']

        for participant in participant_list:
            Participant.objects.create(name=participant, competition=competition)

        return len(participant_list)

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
