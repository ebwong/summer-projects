import flask
from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)

@app.route("/post", methods=["POST"])
def home():
    """
    data = get_census_data.get_census_data()
    response = flask.Response(data)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
    :return:
    """
    response = flask.Response("You sent %s" % request.data)
    # response.headers["Access-Control-Allow-Origin"] = "*"
    return response




if __name__ == "__main__":
    app.run(debug=True, port=5000)