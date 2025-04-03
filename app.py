from flask import Flask, render_template, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS if needed

FALLBACK_TEAMS = [
    "Gujarat Lions",
    "Rising Pune Supergiants",
    "Gujarat Titans",
    "Pune Warriors",
    "Delhi Daredevils",
    "Kochi Tuskers Kerala",
    "Royal Challengers Bangalore",
    "Chennai Super Kings",
    "Rising Pune Supergiant",
    "Mumbai Indians",
    "Deccan Chargers",
    "Delhi Capitals",
    "Punjab Kings",
    "Rajasthan Royals",
    "Kings XI Punjab",
    "Sunrisers Hyderabad",
    "Kolkata Knight Riders",
    "Lucknow Super Giants"
]

@app.route('/')
def home():
    try:
        response = requests.get('http://127.0.0.1:5000/api/teams')
        response.raise_for_status()
        teams = response.json()['teams']
        return render_template('index.html', teams=sorted(teams))
    except requests.exceptions.RequestException as e:
        return render_template('index.html', teams=sorted(FALLBACK_TEAMS), error=str(e))

@app.route('/teamvteam')
def team_vs_team():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    
    # First try to get fresh teams data
    try:
        teams_response = requests.get('http://127.0.0.1:5000/api/teams')
        teams_response.raise_for_status()
        teams = teams_response.json()['teams']
    except Exception as e:
        print(f"Teams API Error: {e}")
        teams = FALLBACK_TEAMS
    
    # Then try to get the team vs team data
    try:
        response = requests.get(f'http://127.0.0.1:5000/api/teamvteam?team1={team1}&team2={team2}')
        response.raise_for_status()
        result = response.json()
    except Exception as e:
        print(f"Team vs Team API Error: {e}")
        result = None
    
    return render_template('index.html', result=result, teams=sorted(teams))

@app.route('/team-record')
def team_record():
    team_name = request.args.get('team')
    
    try:
        # Try to fetch team record data
        response = requests.get(f'http://127.0.0.1:5000/api/team-record?team={team_name}')
        response.raise_for_status()
        result = response.json()
        
        # Extract the specific team's data from the response
        team_result = result.get(team_name)
        if not team_result:
            raise ValueError("No data found for this team")
            
    except Exception as e:
        print(f"Team Record API Error: {e}")
        team_result = None
        team_error = str(e)
    else:
        team_error = None
    
    # Get teams list (same as before)
    try:
        teams_response = requests.get('http://127.0.0.1:5000/api/teams')
        teams_response.raise_for_status()
        teams = teams_response.json()['teams']
    except Exception as e:
        print(f"Teams API Error: {e}")
        teams = FALLBACK_TEAMS
    
    return render_template(
        'index.html',
        teams=sorted(teams),
        team_result=team_result,
        team_error=team_error,
        # Preserve existing variables for team vs team section
        result=request.args.get('result'),
        error=request.args.get('error')
    )

@app.route('/batsman-record')
def batsman_record():
    batsman_name = request.args.get('batsman')
    
    try:
        # Try to fetch batsman record data
        response = requests.get(f'http://127.0.0.1:5000/api/batting-record?batsman={batsman_name}')
        response.raise_for_status()
        result = response.json()
        
        # Extract the specific batsman's data from the response
        batsman_result = result.get(batsman_name)
        if not batsman_result:
            raise ValueError("No data found for this batsman")
            
    except Exception as e:
        print(f"Batsman Record API Error: {e}")
        batsman_result = None
        batsman_error = str(e)
    else:
        batsman_error = None
    
    # Get teams list (for other sections)
    try:
        teams_response = requests.get('http://127.0.0.1:5000/api/teams')
        teams_response.raise_for_status()
        teams = teams_response.json()['teams']
    except Exception as e:
        print(f"Teams API Error: {e}")
        teams = FALLBACK_TEAMS
    
    return render_template(
        'index.html',
        teams=sorted(teams),
        batsman_name=batsman_name,
        batsman_result=batsman_result,
        batsman_error=batsman_error,
        # Preserve existing variables for other sections
        result=request.args.get('result'),
        error=request.args.get('error'),
        team_result=request.args.get('team_result'),
        team_error=request.args.get('team_error')
    )

@app.route('/bowler-record')
def bowler_record():
    bowler_name = request.args.get('bowler')
    
    try:
        # Try to fetch bowler record data
        response = requests.get(f'http://127.0.0.1:5000/api/bowling-record?bowler={bowler_name}')
        response.raise_for_status()
        result = response.json()
        
        # Extract the specific bowler's data from the response
        bowler_result = result.get(bowler_name)
        if not bowler_result:
            raise ValueError("No data found for this bowler")
            
    except Exception as e:
        print(f"Bowler Record API Error: {e}")
        bowler_result = None
        bowler_error = str(e)
    else:
        bowler_error = None
    
    # Get teams list (for other sections)
    try:
        teams_response = requests.get('http://127.0.0.1:5000/api/teams')
        teams_response.raise_for_status()
        teams = teams_response.json()['teams']
    except Exception as e:
        print(f"Teams API Error: {e}")
        teams = FALLBACK_TEAMS
    
    return render_template(
        'index.html',
        teams=sorted(teams),
        bowler_name=bowler_name,
        bowler_result=bowler_result,
        bowler_error=bowler_error,
        # Preserve existing variables for other sections
        result=request.args.get('result'),
        error=request.args.get('error'),
        team_result=request.args.get('team_result'),
        team_error=request.args.get('team_error'),
        batsman_name=request.args.get('batsman_name'),
        batsman_result=request.args.get('batsman_result'),
        batsman_error=request.args.get('batsman_error')
    )



if __name__ == '__main__':
    app.run(debug=True, port=8000)