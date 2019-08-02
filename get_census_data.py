"""
Queries 2014 ASE data
"""
import requests

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from cycler import cycler

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
    business_vars = ["ASECB", "ASECB_TTL", "EMP", "PAYANN", "YIBSZFI", "YIBSZFI_TTL"]
    api_key = "5fff67c7b4559d14fc4adc2da294f674e95c1a3e"

    return query_census(business_url, business_vars, api_key)

def simplify_business_df(df_bus):
    """
    Makes the DataFrame easier to read
    :param df_bus:
    :return:
    """
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

    return df_bus

def add_columns_to_business_df(df):
    """
    Inserts additional columns into the DataFrame
    :param df:
    :return:
    """
    pay_per_emp = df["PAYANN"] / df["EMP"]
    df = df.assign(PAYPEREMP=pay_per_emp)
    return df

def convert_categorical_data_to_numerical_data(df):
    # A mapping of the categorical codes to replace for YIBSZFI
    categories_to_replace = {
        # Use the mean for a range?
        "001": "DROP",
        "311": 1, # < 2 years
        "318": 3, # 2-3 years
        "319": 5, # 4-5 years
        "321": 10, # 6-10 years
        "322": 15, # 11-15 years
        "323": 16 # > 16 years
    }

    # Categorical version
    categories_to_replace = {
        # Use the mean for a range?
        "001": "DROP",
        "311": "<2 years",  # < 2 years
        "318": "2-3 years",  # 2-3 years
        "319": "4-5 years",  # 4-5 years
        "321": "6-10 years",  # 6-10 years
        "322": "11-15 years",  # 11-15 years
        "323": ">16 years"  # > 16 years
    }

    df = df.replace(categories_to_replace)
    df = df[df["YIBSZFI"] != "DROP"] # Drop rows where the YIBSZFI is All

    # df = df[df["YIBSZFI"] != "001"] # Drop rows where the YIBSZFI is All

    return df


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

def plot_business_data(xvar, yvar, df):

    marker = "."
    fig = plt.figure()
    ax = plt.axes()
    colors = [
        "r",
        "#FFA500", # Orange
        "y",
        "g",
        "b",
        "#4B0082", # indigo
        "#EE82EE", # violet
        "c", # cyan
        "m", # magenta
        "#FFD700", # gold
        "#00BFFF", # deep sky blue
        "#000080", # navy
        "#FF1493", # deep pink
        "#FFC0CB", # pink
        "#8B4513", # saddle brown
        "#D2691E", # chocolate
        "#708090", # slate gray
        "#800080", # purple
        "#00FF00", # lime
        "#FA8072", # salmon
        "#DC143C", # crimson
    ]
    my_cycle = cycler(color=colors)
    ax.set_prop_cycle(my_cycle)

    # Get a list of all of the demographic categories
    demographic_categories = df["ASECB_TTL"].unique()

    for category in demographic_categories:
        # Get a DataFrame that belongs to this category
        cat_df = df[df["ASECB_TTL"] == category]
        # Plot this category's data
        ax.plot(cat_df[xvar].values, cat_df[yvar].values, marker, label=category)

    ax.legend(loc="lower right", prop={"size": 6})
    ax.set_xlabel(xvar)
    ax.set_ylabel(yvar)
    ax.set_title(f"{yvar} vs {xvar}")

    plt.show()



def print_owner_data():
    """
    For testing: fetches the Business Owner data
    :return:
    """
    owner_data = get_owner_data()
    owner_cols = ["us", "USBORNCIT"]
    df_own = dataframe_from_census(owner_data, owner_cols)
    df_own = df_own.rename(columns={"ASECBO": "RACE"})
    # Collapse rows with same race code

    print(df_own)

def print_business_data(xvar, yvar):
    """
    For testing: fetches the Business Data
    :return:
    """

    bus_data = get_business_data()
    bus_cols = ["us"] # Drop these columns
    df_bus = dataframe_from_census(bus_data, bus_cols)

    # Make sure numeric data are treated as numbers
    df_bus = df_bus.astype({"EMP": np.int64, "PAYANN": np.int64})

    df_bus = convert_categorical_data_to_numerical_data(df_bus)
    df_bus = add_columns_to_business_df(df_bus)

    # Make sure numeric data are treated as numbers
    # df_bus = df_bus.astype({"YIBSZFI": np.int64})

    # export_dataframe_to_excel(df_bus)
    # export_dataframe_to_csv(df_bus)

    plot_business_data(xvar, yvar, df_bus)


    return df_bus


def export_dataframe_to_csv(df):
    csv_path = "C:\\Users\\Andrew\\PycharmProjects\\census-ase\\business-data.csv"
    df.to_csv(path_or_buf=csv_path)

def export_dataframe_to_excel(df):
    excel_path = "C:\\Users\\Andrew\\PycharmProjects\\census-ase\\business-data.xlsx"
    sheet_name = "Census Business Data"
    df.to_excel(excel_path, sheet_name=sheet_name)

def prompt_user():
    welcome_msg = "Welcome to a tool for investigating data from the 2014 " \
                  "ASE. Choose two different variables from the list below(" \
                  "Type the code in all-caps):"

    print(welcome_msg)

    var_options_msg = "Number of employees: EMP\n" \
                      "Annual payroll: PAYANN\n" "" \
                      "Payroll per employee: PAYPEREMP\n" \
                      "Years in business: YIBSZFI\n"

    var_options = ["EMP", "PAYANN", "PAYPEREMP", "YIBSZFI"]
    print(var_options_msg)

    xvar = None
    yvar = None
    xvar_prompt = "Choose 1 variable to plot on the x-axis:"
    yvar_prompt = "Choose 1 variable to plot on the y-axis"
    var_err_msg_str = " is not a valid variable."

    while True:
        print(xvar_prompt)
        xvar = input()
        if xvar not in var_options:
            print(f"{xvar}" + var_err_msg_str)
            xvar = None
            yvar = None
            continue
        print(yvar_prompt)
        yvar = input()
        if yvar not in var_options:
            print(f"{yvar}" + var_err_msg_str)
            xvar = None
            yvar = None
            continue
        break

    return xvar, yvar


def main():
    """
    Driver function for testing
    :return:
    """
    xvar, yvar = prompt_user()
    print_business_data(xvar, yvar)


if __name__ == "__main__":
    main()