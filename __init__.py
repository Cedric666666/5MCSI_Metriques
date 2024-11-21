from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)   


@app.route('/commits/')
def commits():
    minutes = fetch_commit_minutes()
    minute_counts = {minute: minutes.count(minute) for minute in range(60)}
    plt.figure(figsize=(10, 6))
    plt.bar(minute_counts.keys(), minute_counts.values(), color='#FFD700')
    plt.title('Activité des Commits (minute par minute)', fontsize=16, color='#191970')
    plt.xlabel('Minute de l\'heure', fontsize=14, color='#191970')
    plt.ylabel('Nombre de Commits', fontsize=14, color='#191970')
    plt.xticks(range(0, 60, 5))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    return f'<img src="data:image/png;base64,{graph_url}" alt="Graphique des commits">'


@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})


@app.route("/contact/", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")


@app.route("/histogramme/")
def afficher_histogramme():
    return render_template("histogramme.html")


@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")


@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Commentaire2
  
if __name__ == "__main__":
  app.run(debug=True)
