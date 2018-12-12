from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Competition, Match, Participant


class CompetitionImportForm(forms.Form):
    competition = forms.ModelChoiceField(
        Competition.objects.all(), widget=forms.HiddenInput)
    participant_list = forms.CharField(
        widget=forms.Textarea, label='Zoznam nových účastníkov')

    def __init__(self, *args, **kwargs):
        super(CompetitionImportForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Importuj'))

    def clean_participant_list(self):
        competition = self.cleaned_data.get('competition')
        participant_string = self.cleaned_data.get('participant_list')

        participant_list = []

        for line in participant_string.splitlines():
            if not line.strip():
                continue

            line = line.strip()

            if line in participant_list:
                raise forms.ValidationError(
                    'Účastník {} je v zozname dvakrát!'.format(line))

            participant_list.append(line)

            if Participant.objects.filter(competition=competition, name=line).exists():
                raise forms.ValidationError(
                    'Účastník {} už existuje!'.format(line))

        return participant_list

    def save(self):
        competition = self.cleaned_data.get('competition')
        participant_list = self.cleaned_data.get('participant_list')

        for participant in participant_list:
            Participant.objects.create(
                name=participant, competition=competition)

        return len(participant_list)


class CompetitionSubmitForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['competition', 'winner', 'loser']

    def __init__(self, *args, **kwargs):
        super(CompetitionSubmitForm, self).__init__(*args, **kwargs)

        self.fields['competition'].widget = forms.HiddenInput()

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Odovzdaj'))

    def clean_winner(self):
        cleaned_data = super(CompetitionSubmitForm, self).clean()

        competition = cleaned_data.get('competition')
        winner = cleaned_data.get('winner')

        if winner.competition != competition:
            raise forms.ValidationError(
                'Tento účastník nepatrí k tomuto matboju!')

        return winner

    def clean_loser(self):
        cleaned_data = super(CompetitionSubmitForm, self).clean()

        competition = cleaned_data.get('competition')
        winner = cleaned_data.get('winner')
        loser = cleaned_data.get('loser')

        if loser.competition != competition:
            raise forms.ValidationError(
                'Tento účastník nepatrí k tomuto matboju!')

        if winner == loser:
            raise forms.ValidationError('Vyber niekoho iného ako víťaza!')

        return loser
