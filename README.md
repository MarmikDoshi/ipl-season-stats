# ipl-season-stats
Application developed in DJango to analyse ipl data.

**Pre-requisites:**
- python3
- Django==3.2.6

## Change directory to ipl-season-stats
```
cd ipl-season-stats/
```

## Create build for docker
```
sudo docker-compose build
```

## Activate the container by up command
```
sudo docker-compose up -d
```

## Run the container
```
sudo docker run ipl-season-stats_web
```

## Load the fixtures
```
python manage.py loaddata venues.json
python manage.py loaddata ipl_teams.json
```

## APIs to upload the data
- http://localhost:8000/upload/matches/
- http://localhost:8000/upload/deliveries/

## APIs for the django app
- http://localhost:8000/top_teams/2017/4/
- http://localhost:8000/toss_winner/2017/4/
- http://localhost:8000/max_player_of_match/2017/4/
- http://localhost:8000/highest_wins/2017
- http://localhost:8000/percent_wins/2017
- http://localhost:8000/max_venue/2017
- http://localhost:8000/highest_margin/2017
- http://localhost:8000/highest_margin_wickets/2017