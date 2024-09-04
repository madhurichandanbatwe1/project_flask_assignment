from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your OpenWeatherMap API key
API_KEY = 'api_key'

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    if city:
        weather_data = fetch_weather(city)
        return render_template('weather.html', weather=weather_data, city=city)
    return render_template('index1.html', error="Please enter a city name.")

def fetch_weather(city):
    url = f'http://api.openweathermap.org/data/3.0/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
