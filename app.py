from flask import Flask, render_template, request, session, redirect, url_for
from flask_babel import Babel, _
from bulb_calc import calculate_wet_bulb, get_weather_data, get_forecast_data, get_alert_message

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'pt', 'es']
app.secret_key = 'your_secret_key'

babel = Babel(app)

def get_locale():
    return request.args.get('lang') or session.get('lang') or app.config['BABEL_DEFAULT_LOCALE']

babel.init_app(app, locale_selector=get_locale)

@app.context_processor
def inject_get_locale():
    return dict(get_locale=get_locale)

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
            forecast_data = get_forecast_data(city)
            return render_template("index.html", temperature=temp, humidity=humidity, wet_bulb_temperature=wet_bulb_temp, alert_message=alert_message, city=city, country=country, forecast_data=forecast_data)
        except Exception as e:
            return render_template("index.html", error=str(e))
    return render_template("index.html")

@app.route('/change-language')
def change_language():
    lang = request.args.get('lang')
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        session['lang'] = lang
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
