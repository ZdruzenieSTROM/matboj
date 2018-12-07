from django.urls import path

from .views import (CompetitionDetailView, CompetitionImportView,
                    CompetitionListView, CompetitionResultsView,
                    CompetitionSubmitView)

app_name = 'competition'

urlpatterns = [
    path('', CompetitionListView.as_view(), name='index'),
    path('matboj/<int:pk>', CompetitionDetailView.as_view(), name='competition'),
    path('matboj/<int:pk>/import', CompetitionImportView.as_view(), name='import'),
    path('matboj/<int:pk>/results', CompetitionResultsView.as_view(), name='results'),
    path('matboj/<int:pk>/submit', CompetitionSubmitView.as_view(), name='submit'),
]
