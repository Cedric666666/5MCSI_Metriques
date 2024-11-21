import requests
from datetime import datetime

def fetch_commit_minutes():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"Erreur de connexion avec l'API, code : {response.status_code}"

    commits = response.json()
    minutes = []

    for commit in commits:
        commit_date = commit["commit"]["author"]["date"]
        date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
        minutes.append(date_object.minute)

    return minutes
