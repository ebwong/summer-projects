from flask import Flask, request, Response
from flask_cors import CORS
from census_backend import get_census_data

app = Flask(__name__)
# Enable CORS for the server
cors = CORS(app)

@app.route("/flask-endpoint", methods=["POST"])
def get_react_data():
    # Get the chosen variable from React
    react_data = request.json
    chosen_var = react_data["chosenVar"]
    data = get_census_data.get_census_data(chosen_var)
    response = Response(data)
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000)