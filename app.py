from flask import Flask, render_template, request
from bulb_calc import calculate_wet_bulb, get_weather_data, get_alert_message

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form["city"]
        try:
            weather_data = get_weather_data(city)
            temp = weather_data['temperature']
            humidity = weather_data['humidity']
            country = weather_data['country']
            wet_bulb_temp = calculate_wet_bulb(temp, humidity)
            alert_message = get_alert_message(wet_bulb_temp)
            return render_template("index.html", temperature=temp, humidity=humidity, wet_bulb_temperature=wet_bulb_temp, alert_message=alert_message, city=city, country=country)
        except Exception as e:
            return render_template("index.html", error=str(e))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
