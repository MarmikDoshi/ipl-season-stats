from django.db import models

# Create your models here.


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class Venue(models.Model):
    """Data of a venue."""
    venue_id = models.AutoField(primary_key=True)
    venue = models.CharField(max_length=100)
    city = models.CharField(max_length=50)


class Match(models.Model):
    """Data of a match."""
    TOSS_DECISION = (('FIELD', 'Field'), ('BAT', 'Bat'))

    RESULT = (('NO_RESULT', 'No Result'), ('TIE', 'Tie'), ('NORMAL', 'Normal'))

    match_id = models.IntegerField()
    season = models.IntegerField()
    date = models.DateField()
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_one')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_two')
    toss_winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='toss_winner')
    toss_decision = models.CharField(max_length=10, choices=TOSS_DECISION)
    result = models.CharField(max_length=15, choices=RESULT)
    dl_applied = models.BooleanField()
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_winner', null=True)
    win_by_runs = models.CharField(max_length=10, null=True, blank=True)
    win_by_wickets = models.CharField(max_length=10, null=True, blank=True)
    player_of_match = models.CharField(max_length=50, null=True, blank=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    umpire1 = models.CharField(max_length=50)
    umpire2 = models.CharField(max_length=50)
    umpire3 = models.CharField(max_length=50)


class Delivery(models.Model):
    """Data of a delivery."""

    class Inning(models.IntegerChoices):
        FIRST = 1
        SECOND = 2

    DISMISSAL_KIND = (('CAUGHT', 'caught'), ('BOWLED', 'bowled'), ('LBW', 'lbw'),
                      ('C&B', 'Caught and Bowled'), ('RUN_OUT', 'Run Out'), ('STUMPED', 'stumped'))

    match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
    inning = models.IntegerField(choices=Inning.choices)
    batting_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='batting_team')
    bowling_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='bowling_team')
    over = models.IntegerField()
    ball = models.IntegerField()
    batsman = models.CharField(max_length=50)
    non_striker = models.CharField(max_length=50)
    bowler = models.CharField(max_length=50)
    is_super_over = models.BooleanField()
    wide_runs = models.IntegerField()
    bye_runs = models.IntegerField()
    legbye_runs = models.IntegerField()
    noball_runs = models.IntegerField()
    penalty_runs = models.IntegerField()
    batsman_runs = models.IntegerField()
    extra_runs = models.IntegerField()
    total_runs = models.IntegerField()
    player_dismissed = models.CharField(max_length=50, null=True, blank=True)
    dismissal_kind = models.CharField(max_length=50, choices=DISMISSAL_KIND)
    fielder = models.CharField(max_length=50)






