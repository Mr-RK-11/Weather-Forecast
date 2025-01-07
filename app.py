from flask import Flask, render_template, request, jsonify
import requests
from collections import defaultdict
import os

app = Flask(__name__)

API_KEY = '946a915a7bba4fdb8d201b991abde4a3'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    if city:
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url).json()

        if response['cod'] == "200":
            grouped_weather = defaultdict(list)
            for item in response['list']:
                date = item['dt_txt'].split(' ')[0]
                data = {
                    'date_time': item['dt_txt'],
                    'temperature': round(item['main']['temp']),
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'],
                    'wind_speed': item['wind']['speed'],
                    'icon': item['weather'][0]['icon']
                }
                grouped_weather[date].append(data)
            return jsonify(dict(grouped_weather))
        else:
            return jsonify({'error': 'City not found'})
    return jsonify({'error': 'No city provided'})

if __name__ == '__main__':
    # Only open browser in development
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

    
