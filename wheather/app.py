from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        place = request.form.get("place")
        if place:
            try:
                url = f"http://goweather.xyz/weather/{place}"
                resp = requests.get(url, timeout=6)
                if resp.status_code == 200:
                    data = resp.json()
                    result = {
                        "place": place.title(),
                        "temperature": data.get("temperature"),
                        "wind": data.get("wind"),
                        "description": data.get("description")
                    }
                else:
                    result = {"error": "Weather source returned error."}
            except requests.RequestException:
                result = {"error": "Failed to fetch weather data."}
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
