"""
Queries 2014 ASE data
"""
import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_census_var_string(census_vars):
    """
    Generates a formatted string of the variables to query for

    :param census_vars: a tuple of variables to join
    :return: a string containing the variables delimited by commas
    """

    if len(census_vars) == 1:
        return census_vars
    delimiter = ","
    return delimiter.join(census_vars)

def query_census(url, census_vars):
    """
    Returns census data as a list of JSON objects
    :param url: the URL containing the census data
    :param census_vars: a tuple of census variables to query for
    :return: census data in as a list of JSON objects
    """

    census_var_string = get_census_var_string(census_vars)
    params = {
        "get": census_var_string,
        "for": "us:*" # in the entire U.S.
    }
    response = requests.get(url, params=params)
    # print(response.status_code)
    # print(response.content)
    return response.json()

def format_census_data(census_data):
    """
    Formats the census data as a Pandas Dataframe
    :param census_data: the given census data
    :return: census data as a Pandas Dataframe
    """

    census_data_as_list_of_dicts = []
    # The first element is always the headers
    census_data_labels = census_data[0]
    for i in range(1, len(census_data)):
        # Zip the two lists (headers : values), convert to a dict, and append
        # to list
        census_data_as_list_of_dicts.append(pd.Series(
            dict(zip(census_data_labels, census_data[i]))))
    return pd.DataFrame(census_data_as_list_of_dicts)

def format_census_data_for_graphing(census_data):
    data = []
    pass

def plot_data(data):
    x_spacing = np.arange(len(data[1]))
    plt.bar(x_spacing, data[1])
    plt.xlabel("Education")
    plt.ylabel("Number of business owners")

    plt.xticks(x_spacing, data[0], fontsize=5, rotation=30)

    plt.title("Education vs number of business owners")
    plt.show()

def get_census_data():
    url = "https://api.census.gov/data/2014/ase/cscbo"
    census_vars = ("OWNPDEMP", "HRSWRKD", "HRSWRKD_TTL", "YIBSZFI",
                   "YIBSZFI_TTL", "USBORNCIT", "USBORNCIT_TTL")  # The variables to query for
    return query_census(url, census_vars)

data = format_census_data(get_census_data())
filtered_data = data.query(" HRSWRKD == 'CZ' ")
# print(filtered_data["YIBSZFI_TTL"])
# print(data.index.values)




run_tests = False
if run_tests:
    data = format_census_data(get_census_data())
    print(data)
    plot_data(data)

output_to_file = False
if output_to_file:
    output = format_census_data(get_census_data())
    file = open(".\output.txt", mode="w+")
    file.write(str(output))
    file.close()




