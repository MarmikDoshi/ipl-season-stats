import csv

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.db.models import Count, Max
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView
from django.urls import reverse

from iplstats.models import Delivery, Match, Team, Venue


class UploadMatches(View):
    def get(self, request):
        return render(request, "upload_matches.html")

    def post(self, request):
        """Method to upload data of matches."""
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            print(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("iplstats:UploadMatches"))

        matches = []

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            try:
                winner = None
                team1 = Team.objects.get(name=row['team1'])
                team2 = Team.objects.get(name=row['team2'])
                toss_winner = Team.objects.get(name=row['toss_winner'])
                if row['winner']:
                    winner = Team.objects.get(name=row['winner'])
                venue = Venue.objects.get(venue=row['venue'])
                match = Match(match_id=row['id'], season=row['season'], date=row['date'], team1=team1, team2=team2,
                              toss_winner=toss_winner, toss_decision=row['toss_decision'],
                              result=row['result'], dl_applied=row['dl_applied'],
                              winner=winner, win_by_runs=row['win_by_runs'], win_by_wickets=row['win_by_wickets'],
                              player_of_match=row['player_of_match'], venue=venue, umpire1=row['umpire1'],
                              umpire2=row['umpire2'], umpire3=row['umpire3'])
                matches.append(match)

            except ObjectDoesNotExist:
                print("Entry doesn't exist.", row)

        Match.objects.bulk_create(matches)
        return HttpResponseRedirect(reverse("iplstats:UploadMatches"))


class UploadDeliveries(View):
    def get(self, request):
        return render(request, "upload_deliveries.html")

    def post(self, request):
        """Method to upload data of deliveries."""
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            print(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("iplstats:UploadDeliveries"))

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        deliveries = []

        for row in reader:
            try:
                match_id = Match.objects.get(match_id=row['match_id'])
                batting_team = Team.objects.get(name=row['batting_team'])
                bowling_team = Team.objects.get(name=row['bowling_team'])
                delivery = Delivery(
                    match_id=match_id, inning=row['inning'],
                    batting_team=batting_team, bowling_team=bowling_team,
                    over=row['over'], ball=row['ball'], batsman=row['batsman'],
                    non_striker=row['non_striker'], bowler=row['bowler'],
                    is_super_over=row['is_super_over'], wide_runs=row['wide_runs'],
                    bye_runs=row['bye_runs'], legbye_runs=row['legbye_runs'],
                    noball_runs=row['noball_runs'], penalty_runs=row['penalty_runs'],
                    batsman_runs=row['batsman_runs'], extra_runs=row['extra_runs'],
                    total_runs=row['total_runs'], player_dismissed=row['player_dismissed'],
                    dismissal_kind=row['dismissal_kind'], fielder=row['fielder']
                )
                deliveries.append(delivery)

            except ObjectDoesNotExist:
                print("Entry doesn't exist.", row)

        Delivery.objects.bulk_create(deliveries)
        return HttpResponseRedirect(reverse("iplstats:UploadDeliveries"))


def get_season_records(season):
    matches = Match.objects.filter(season=season)
    return matches


class TopTeamsView(ListView):
    model = Match

    def get(self, *args, **kwargs):
        """Method to get top teams in terms of wins."""
        season_matches = get_season_records(kwargs['season'])
        winners = season_matches.values('winner__name').annotate(total_wins=Count('winner')).order_by(
            '-total_wins')[:int(kwargs['number_of_teams'])]

        return JsonResponse({"winners_list": list(winners)})


class TossWinnerView(ListView):
    model = Match

    def get(self, *args, **kwargs):
        """Method to get team who won most number of tosses."""
        season_matches = get_season_records(kwargs['season'])
        toss_winners = season_matches.values('toss_winner__name').annotate(total=Count('toss_winner')).order_by(
            '-total')[:int(kwargs['number_of_teams'])]

        return JsonResponse({"winners_list": list(toss_winners)})


class MaxPlayerofMatch(ListView):
    model = Match

    def get(self, *args, **kwargs):
        """Method to get player who won max number of awards."""
        season_matches = get_season_records(kwargs['season'])
        players = season_matches.values('player_of_match').annotate(total=Count('player_of_match')).order_by(
            '-total')[:int(kwargs['number_of_teams'])]

        return JsonResponse({"winners_list": list(players)})


class HighestWins(ListView):
    model = Match

    def get(self, *args, **kwargs):
        """Method to get team who won max number of matches."""
        season_matches = get_season_records(kwargs['season'])
        winners = season_matches.values('winner__name').annotate(total_wins=Count('winner')).order_by(
            '-total_wins')[:1]

        return JsonResponse({"winners_list": list(winners)})


class PercentWins(ListView):
    model = Match

    def get(self, *args, **kwargs):
        """Method to get percentage of teams who decided to bat."""
        total_count = Match.objects.filter(season=kwargs['season']).count()

        bat_count = Match.objects.filter(toss_decision='bat', season=kwargs['season']).count()

        perc = bat_count * 100 / total_count

        return JsonResponse({"winners_list": perc})


class MaxVenue(ListView):
    model = Match

    def get(self, *args, **kwargs):
        """Method to get location which hosted most number of matches."""
        season_matches = get_season_records(kwargs['season'])
        venues = season_matches.values('venue__venue').annotate(total=Count('venue')).order_by('-total')[:1]

        return JsonResponse({"winners_list": list(venues)})


class HighestMarginofRuns(ListView):
    model = Match

    def get(self, *args, **kwargs):
        """Method to get team who won by highest margin of runs."""
        season_matches = get_season_records(kwargs['season'])
        team = season_matches.aggregate(Max('win_by_runs'))

        return JsonResponse(team)


class HighestMarginofWickets(ListView):
    model = Match

    def get(self, *args, **kwargs):
        """Method to get team who won by highest margin of wickets."""
        season_matches = get_season_records(kwargs['season'])
        team = season_matches.aggregate(Max('win_by_wickets'))

        return JsonResponse(team)
