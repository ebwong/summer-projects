# The endpoint queried by the front end. It queries the U.S. Census API
# with the given variables and returns a JSON response.

from flask import Flask, request, Response
from flask_cors import CORS
from census_backend import get_census_data

# The names of the independent and dependent variables given by the frontend
INDEPENDENT_VAR_KEY = "independentVar"
DEPENDENT_VAR_KEY = "dependentVar"

app = Flask(__name__)
# Enable CORS for the server
cors = CORS(app)

@app.route("/flask-endpoint", methods=["POST"])
def get_react_data():
    independent_var = request.json[INDEPENDENT_VAR_KEY]
    dependent_var = request.json[DEPENDENT_VAR_KEY]
    data = get_census_data.get_census_data(independent_var, dependent_var)
    response = Response(data)
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000)