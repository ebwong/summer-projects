"""
Queries 2014 ASE data
"""
import requests
import matplotlib
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

def query_census(url, census_vars, api_key=None):
    """
    Returns census data as a list of JSON objects
    :param url: the URL containing the census data
    :param census_vars: a tuple of census variables to query for
    :param api_key: An API key for using the Census API; defaults to None
    :return: census data  as a list of JSON objects
    """

    census_var_string = get_census_var_string(census_vars)
    params = {
        "get": census_var_string,
        "for": "us:*", # in the entire U.S.
        "key": api_key
    }
    response = requests.get(url, params=params)
    return response.json()

def dataframe_from_census(census_data, columns_to_drop=None):
    """
    Formats the census data as a Pandas DataFrame
    :param census_data: the given census data
    :param columns_to_drop: columns to omit from the returned DataFrame
    :return: census data as a Pandas DataFrame
    """

    census_data_as_list_of_dicts = []
    # The first element is always the headers
    census_data_labels = census_data[0]
    for i in range(1, len(census_data)):
        # Zip the two lists (headers : values), convert to a dict, and append
        # to list
        census_data_as_list_of_dicts.append(pd.Series(
            dict(zip(census_data_labels, census_data[i]))))

    df_census = pd.DataFrame(census_data_as_list_of_dicts)
    # Get rid of some unnecessary columns
    return df_census.drop(columns=columns_to_drop)



def format_owner_data_for_graphing(census_data):
    x_var = [elem for elem in census_data["YIBSZFI_TTL"]]
    y_var = [int(elem, 10) for elem in census_data["OWNPDEMP"]]
    return [x_var, y_var]


def plot_owner_data(data):
    x_var_index = 0
    y_var_index = 1
    x_label = "Years in business"
    y_label = "Number of business owners"
    x_spacing = np.arange(len(data[x_var_index]))
    plt.bar(x_spacing, data[y_var_index])
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.xticks(x_spacing, data[y_var_index], fontsize=5, rotation=30)

    plt.title(f"{x_label} vs {y_label}")
    plt.show()


def get_owner_data():
    """
    Returns Census ASE Business Owner data
    :return:
    """

    owner_url = "https://api.census.gov/data/2014/ase/cscbo"
    owner_vars = ("ASECBO", "ASECBO_TTL", "OWNPDEMP", "USBORNCIT")  # The variables to query for
    api_key = "5fff67c7b4559d14fc4adc2da294f674e95c1a3e"
    return query_census(owner_url, owner_vars, api_key)

def get_business_data():
    """
    Returns Census ASE Business data
    :return:
    """

    business_url = "https://api.census.gov/data/2014/ase/cscb"
    business_vars = ("ASECB", "ASECB_TTL", "EMP", "PAYANN", "YIBSZFI")
    api_key = "5fff67c7b4559d14fc4adc2da294f674e95c1a3e"

    return query_census(business_url, business_vars, api_key)

def simplify_business_df(df_bus):
    # Formatting business data
    df_bus = df_bus.rename(columns={"ASECB": "RACE"})
    # Make codes uniform
    # A mapping of the codes to replace
    bus_codes_to_replace = {
        "0000": "00",
        "0001": "01",
        "0002": "02",
        "0010": "20",
        "0030": "29",
        "0100": "30",
        "0200": "40",
        "0300": "50",
        "0400": "60",
        "0500": "70",
        "0600": "80",
        "0700": "90",
        "0900": "92",
        "1000": "V2",
        "3000": "V4",
    }

    # Rename codes that should be kept
    df_bus = df_bus.replace(bus_codes_to_replace)

    # Remove extraneous rows
    bus_codes_to_remove = [
        "0003", "0020", "0800", "2000", "9996", "9998"
    ]
    df_bus = df_bus[np.logical_not(df_bus["RACE"].isin(bus_codes_to_remove))]

    # Make sure numeric data are treated as numbers
    df_bus = df_bus.astype({"EMP": np.int64, "PAYANN": np.int64})

    return df_bus

def add_columns_to_business_df(df_bus):
    pay_per_emp = df_bus["PAYANN"] // df_bus["EMP"]


    df_bus = df_bus.assign(PAYPEREMP= pay_per_emp)
    return df_bus

def main():
    owner = False
    if owner:
        owner_data = get_owner_data()
        owner_cols = ["us", "USBORNCIT"]
        df_own = dataframe_from_census(owner_data, owner_cols)
        df_own = df_own.rename(columns={"ASECBO": "RACE"})
        # Collapse rows with same race code


        print(df_own)

    bus = True
    if bus:
        bus_data = get_business_data()
        bus_cols = ["us"]
        df_bus = dataframe_from_census(bus_data, bus_cols)
        df_bus = simplify_business_df(df_bus)
        df_bus = add_columns_to_business_df(df_bus)


        print(df_bus)

        # print(df_bus.to_csv())






if __name__ == "__main__":
    main()








run_tests = False
if run_tests:
    data = dataframe_from_census(get_owner_data())
    filtered_data = data.query(" HRSWRKD == 'CZ' ")
    plot_owner_data(format_owner_data_for_graphing(filtered_data))

output_to_file = False
if output_to_file:
    output = dataframe_from_census(get_owner_data())
    file = open(".\output.txt", mode="w+")
    file.write(str(output))
    file.close()




