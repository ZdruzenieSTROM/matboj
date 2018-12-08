from math import floor
from operator import itemgetter

from django.contrib import messages
from django.shortcuts import reverse
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.detail import SingleObjectMixin

from .forms import CompetitionImportForm, CompetitionSubmitForm
from .models import Competition, Match, Participant


class CompetitionListView(ListView):
    model = Competition
    context_object_name = 'competitions'

    template_name = 'competition/index.html'

class CompetitionDetailView(DetailView):
    model = Competition
    context_object_name = 'competition'

    template_name = 'competition/competition.html'

class CompetitionImportView(FormView, SingleObjectMixin):
    model = Competition
    context_object_name = 'competition'

    template_name = 'competition/import.html'

    form_class = CompetitionImportForm

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super(CompetitionImportView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(CompetitionImportView, self).get_initial()
        initial.update({'competition': self.object})
        return initial

    def get_success_url(self):
        return reverse('competition:competition', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        imported = form.save()

        messages.success(self.request, 'Počet pridaných účastníkov: {}'.format(imported))

        return super(CompetitionImportView, self).form_valid(form)

class CompetitionResultsView(DetailView):
    model = Competition
    context_object_name = 'competition'

    template_name = 'competition/results.html'

    def get_context_data(self, **kwargs):
        context_data = super(CompetitionResultsView, self).get_context_data(**kwargs)

        scores = {
            participant: 1000
            for participant in self.object.participant_set.all()
        }

        matches = Match.objects.filter(competition=self.object).order_by('time')

        for match in matches:
            scores[match.winner] = scores[match.winner] + floor(0.1*scores[match.loser])
            scores[match.loser] = scores[match.loser] - floor(0.1*scores[match.loser])

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

class CompetitionSubmitView(FormView, SingleObjectMixin):
    model = Competition
    context_object_name = 'competition'

    template_name = 'competition/submit.html'

    form_class = CompetitionSubmitForm

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super(CompetitionSubmitView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(CompetitionSubmitView, self).get_context_data(**kwargs)
        context_data['history'] = Match.objects.order_by('-time')[:10]
        return context_data

    def get_success_url(self):
        return reverse('competition:submit', kwargs={'pk': self.kwargs['pk']})

    def get_initial(self):
        initial = super(CompetitionSubmitView, self).get_initial()
        initial.update({'competition': self.object})
        return initial

    def get_form(self, form_class=None):
        form = super(CompetitionSubmitView, self).get_form(form_class=form_class)

        form.fields['winner'].queryset = Participant.objects.filter(
            competition=form.initial['competition']
        )

        form.fields['loser'].queryset = Participant.objects.filter(
            competition=form.initial['competition']
        )

        return form

    def form_valid(self, form):
        form.save()

        return super(CompetitionSubmitView, self).form_valid(form)
