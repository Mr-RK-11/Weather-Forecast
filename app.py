from flask import Flask, render_template, request, jsonify #webframework
import requests #retieve data from API
from collections import defaultdict #
import webbrowser
import time
import threading

app = Flask(__name__)

API_KEY = '946a915a7bba4fdb8d201b991abde4a3'

@app.route('/')
def home():
    return render_template('index.html')
def open_browser():
    # Give Flask time to start before opening the browser
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000")
@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    if city:
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url).json()

        if response['cod'] == "200":  
            grouped_weather = defaultdict(list)

            for item in response['list']:
                date = item['dt_txt'].split(' ')[0]  # Extract date only (YYYY-MM-DD)
                data = {
                    'date_time': item['dt_txt'],
                    'temperature': round(item['main']['temp']),
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'],
                    'wind_speed': item['wind']['speed'],
                    'icon': item['weather'][0]['icon']
                }
                grouped_weather[date].append(data)

            return jsonify(dict(grouped_weather))  # Convert to regular dict
        else:
            return jsonify({'error': 'City not found'})
    return jsonify({'error': 'No city provided'})

if __name__ == '__main__':
    # Start the browser opening in a separate thread
    threading.Thread(target=open_browser).start()
    
    # Run the Flask web server
    app.run(debug=True, use_reloader=False)