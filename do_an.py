from flask import Flask, request
import requests

app = Flask(__name__)

def get_weather_data(city_name):
    api_key = "22b7f3537fa4da3978cdd4360f888378"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"
    
    response = requests.get(complete_url)
    data = response.json()
    
    if response.status_code == 200:
        main = data["main"]
        sys = data["sys"]
        weather = data["weather"][0]
        wind = data["wind"]
        
        weather_data = {
            "location_name": f"{data['name']}, {sys['country']}",
            "temperature": main["temp"],
            "weather_description": weather["description"].capitalize(),
            "humidity": main["humidity"],
            "wind_speed": wind["speed"],
        }
        return weather_data
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None
    if request.method == "POST":
        city_name = request.form["city_name"]
        weather_data = get_weather_data(city_name)
        if weather_data is None:
            error = "City not found or API error"
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weather App</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Poppins', sans-serif;
            }}
            body {{
                background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #444;
                position: relative;
            }}
            .container {{
                background-color: rgba(255, 255, 255, 0.85);
                border-radius: 15px;
                padding: 40px;
                width: 450px;
                text-align: center;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                font-size: 30px;
                margin-bottom: 20px;
                color: #333;
            }}
            form {{
                display: flex;
                justify-content: center;
                gap: 10px;
                margin-bottom: 20px;
            }}
            input[type="text"] {{
                padding: 12px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 16px;
                width: 250px;
                transition: border-color 0.3s ease;
            }}
            input[type="text"]:focus {{
                border-color: #1f78d1;
                outline: none;
            }}
            button {{
                padding: 12px 24px;
                background-color: #1f78d1;
                border: none;
                color: white;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
                transition: transform 0.3s ease, background-color 0.3s ease;
                transform: perspective(1px) translateZ(0);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            button:hover {{
                background-color: #145a99;
                transform: scale(1.1);
            }}
            button:active {{
                transform: scale(1.05);
            }}
            h2 {{
                color: #1f78d1;
                margin-bottom: 15px;
                font-size: 22px;
            }}
            p {{
                font-size: 18px;
                color: #555;
            }}
            .error {{
                color: red;
                margin-top: 15px;
            }}
            .footer {{
                position: absolute;
                bottom: 10px;
                right: 10px;
                font-size: 14px;
                color: #888;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Weather Information</h1>
            <form action="/" method="POST">
                <input type="text" name="city_name" placeholder="Enter city name" required>
                <button type="submit">Get Weather</button>
            </form>
    """
    
    if weather_data:
        html += f"""
        <h2>Location: {weather_data['location_name']}</h2>
        <p>Temperature: {weather_data['temperature']}°C</p>
        <p>Weather: {weather_data['weather_description']}</p>
        <p>Humidity: {weather_data['humidity']}%</p>
        <p>Wind Speed: {weather_data['wind_speed']} m/s</p>
        """
    elif error:
        html += f"<p class='error'>Error: {error}</p>"
    
    html += """
        </div>
        <div class="footer">
            Nhóm 3: Print current weather information for a city
        </div>
    </body>
    </html>
    """
    
    return html

if __name__ == "__main__":
    app.run(debug=True)
