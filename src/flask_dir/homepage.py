from flask import Flask, render_template, request, send_file
from src import get_census_data

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("home.html")

@app.route('/census-data')
def return_census_img():
    try:
        path = get_census_data.get_census_data()
        return send_file(path, attachment_filename='census.png')
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)