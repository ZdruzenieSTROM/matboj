from math import floor
from operator import itemgetter

from django.contrib import messages
from django.shortcuts import reverse
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.detail import SingleObjectMixin

from .forms import CompetitionImportForm, CompetitionSubmitForm
from .models import Competition, Match, Participant


class SingleObjectFormView(FormView, SingleObjectMixin):
    object_field_name = None

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super(SingleObjectFormView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SingleObjectFormView, self).get_form_kwargs()

        if self.request.method in ('POST', 'PUT'):
            data = kwargs['data'].copy()
            data[self.object_field_name] = str(self.object.pk)
            kwargs['data'] = data

        if self.request.method == 'GET':
            kwargs['initial'].update({self.object_field_name: self.object})

        return kwargs


class CompetitionListView(ListView):
    model = Competition
    context_object_name = 'competitions'

    template_name = 'competition/index.html'


class CompetitionDetailView(DetailView):
    model = Competition
    context_object_name = 'competition'

    template_name = 'competition/competition.html'


class CompetitionImportView(SingleObjectFormView):
    model = Competition
    context_object_name = 'competition'

    template_name = 'competition/import.html'

    form_class = CompetitionImportForm

    object_field_name = 'competition'

    def get_success_url(self):
        return reverse('competition:competition', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        imported = form.save()

        messages.success(
            self.request, 'Počet pridaných účastníkov: {}'.format(imported))

        return super(CompetitionImportView, self).form_valid(form)


class CompetitionResultsView(DetailView):
    model = Competition
    context_object_name = 'competition'

    template_name = 'competition/results.html'

    def get_context_data(self, **kwargs):
        context_data = super(CompetitionResultsView,
                             self).get_context_data(**kwargs)

        scores = {
            participant: 1000
            for participant in self.object.participant_set.all()
        }

        matches = Match.objects.filter(
            competition=self.object).order_by('time')

        for match in matches:
            scores[match.winner] = scores[match.winner] + \
                floor(0.1*scores[match.loser])
            scores[match.loser] = scores[match.loser] - \
                floor(0.1*scores[match.loser])

        rankings = sorted(
            [
                {'participant': participant, 'score': score, 'rank': 1}
                for participant, score in scores.items()
            ],
            key=itemgetter('score'),
            reverse=True
        )

        for i, ranking in enumerate(rankings[1:]):
            if ranking['score'] == rankings[i]['score']:
                rankings[i+1]['rank'] = rankings[i]['rank']
            else:
                rankings[i+1]['rank'] = rankings[i]['rank'] + 1

        context_data['rankings'] = rankings

        return context_data


class CompetitionSubmitView(SingleObjectFormView):
    model = Competition
    context_object_name = 'competition'

    template_name = 'competition/submit.html'

    form_class = CompetitionSubmitForm

    object_field_name = 'competition'

    def get_context_data(self, **kwargs):
        context_data = super(CompetitionSubmitView,
                             self).get_context_data(**kwargs)

        context_data['history'] = Match.objects.filter(
            competition=self.object).order_by('-time')

        return context_data

    def get_success_url(self):
        return reverse('competition:submit', kwargs={'pk': self.kwargs['pk']})

    def get_form(self, form_class=None):
        form = super(CompetitionSubmitView, self).get_form(
            form_class=form_class)

        form.fields['winner'].queryset = Participant.objects.filter(
            competition=self.object)

        form.fields['loser'].queryset = Participant.objects.filter(
            competition=self.object)

        return form

    def form_valid(self, form):
        form.save()

        return super(CompetitionSubmitView, self).form_valid(form)
