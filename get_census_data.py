import requests
import matplotlib.pyplot as plt
import numpy as np


def generateVarString(vars):
    """

    :param vars: a tuple of variables to join
    :return: a string containing the variables delimited by commas
    """
    if len(vars) == 1:
        return vars
    delimiter = ","
    return delimiter.join(vars)

def get_data():
    url = "https://api.census.gov/data/2014/ase/cscbo"
    vars = ("OWNPDEMP", "EDUC", "EDUC_TTL")
    varString = generateVarString(vars)
    params = {
        "get": varString,
        "for": "us:*" # in the entire U.S.
    }
    response = requests.get(url, params=params)
    return response.json()

def parse_data(data):
    x_index = 2
    y_index = 0
    xvals = []
    yvals = []
    for i in range(1, len(data) - 2):
        xvals.append(data[i][x_index])
        yvals.append(int(data[i][y_index], 10))

    # Organize the data

    return [xvals, yvals]

def plot_data(data):
    x_spacing = np.arange(len(data[1]))
    plt.bar(x_spacing, data[1])
    plt.xlabel("Education")
    plt.ylabel("Number of business owners")

    plt.xticks(x_spacing, data[0], fontsize=5, rotation=30)

    plt.title("Education vs number of business owners")
    plt.show()


data = parse_data(get_data())
print(data)
plot_data(data)




