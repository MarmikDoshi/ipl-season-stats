from django.conf.urls import url

from iplstats import views

urlpatterns = [
    url(r'^upload/matches/$', views.UploadMatches.as_view(), name='UploadMatches'),
    url(r'^upload/deliveries/$', views.UploadDeliveries.as_view(), name='UploadDeliveries'),
    url(r'^top_teams/(?P<season>[0-9]{4})/(?P<number_of_teams>[0-9]+)/', views.TopTeamsView.as_view(),
        name='TopTeamsView'),
    url(r'^toss_winner/(?P<season>[0-9]{4})/(?P<number_of_teams>[0-9]+)/', views.TossWinnerView.as_view(),
        name='TossWinnerView'),
    url(r'^max_player_of_match/(?P<season>[0-9]{4})/(?P<number_of_teams>[0-9]+)/', views.MaxPlayerofMatch.as_view(),
        name='MaxPlayerofMatch'),
    url(r'^highest_wins/(?P<season>[0-9]{4})', views.HighestWins.as_view(),
        name='HighestWins'),
    url(r'^percent_wins/(?P<season>[0-9]{4})', views.PercentWins.as_view(),
        name='PercentWins'),
    url(r'^max_venue/(?P<season>[0-9]{4})', views.MaxVenue.as_view(),
        name='MaxVenue'),
    url(r'^highest_margin/(?P<season>[0-9]{4})', views.HighestMarginofRuns.as_view(),
        name='HighestMarginofRuns'),
    url(r'^highest_margin_wickets/(?P<season>[0-9]{4})', views.HighestMarginofWickets.as_view(),
        name='HighestMarginofWickets')
]



