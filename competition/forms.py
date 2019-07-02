from operator import methodcaller

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
        participant_string = self.cleaned_data.get('participant_list')

        participant_list = []
        errors = []

        for line in filter(lambda l: len(l) != 0, map(
                methodcaller('strip'), participant_string.splitlines())):
            if line in participant_list:
                error = "Účastník {} je v zozname viackrát!".format(line)

                if error not in errors:
                    errors.append(error)

                continue

            participant_list.append(line)

        if errors:
            raise forms.ValidationError(errors)

        return participant_list

    def clean(self):
        cleaned_data = super(CompetitionImportForm, self).clean()

        competition = cleaned_data.get('competition')
        participant_list = cleaned_data.get('participant_list')

        if competition and participant_list:
            for participant in participant_list:
                if Participant.objects.filter(competition=competition, name=participant).exists():
                    self.add_error('participant_list',
                                   'Účastník {} už existuje!'.format(participant))

        return cleaned_data

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

    def clean(self):
        cleaned_data = super(CompetitionSubmitForm, self).clean()

        competition = cleaned_data.get('competition')
        winner = cleaned_data.get('winner')
        loser = cleaned_data.get('loser')

        if all((competition, winner, loser)):
            if winner == loser:
                raise forms.ValidationError(
                    'Víťaz a porazený sú tá istá osoba!')

        return cleaned_data
