from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from .views import (CompetitionDetailView, CompetitionImportView,
                    CompetitionListView, CompetitionResultsView,
                    CompetitionSubmitView)

app_name = 'competition'

urlpatterns = [
    path('', CompetitionListView.as_view(), name='index'),
    path('matboj/<int:pk>',
         staff_member_required(CompetitionDetailView.as_view()), name='competition'),
    path('matboj/<int:pk>/import',
         staff_member_required(CompetitionImportView.as_view()), name='import'),
    path('matboj/<int:pk>/results',
         staff_member_required(CompetitionResultsView.as_view()), name='results'),
    path('matboj/<int:pk>/submit',
         staff_member_required(CompetitionSubmitView.as_view()), name='submit'),
]
