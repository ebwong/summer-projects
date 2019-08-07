"""
Main module for querying 2014 ASE data and 2012 Survey of Business Owners
"""
import requests
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from cycler import cycler

# Data exporting modules
from src.census_data_export import export_dataframes_to_excel
from src.census_data_export import export_dataframe_to_csv

# Data formatting modules
from src.census_data_formatting import get_columns_to_rename
from src.census_data_formatting import get_columns_to_drop
from src.census_data_formatting import convert_categorical_data_to_numerical_data

# Data visualization modules
from src.census_data_plotting import plot_business_data


def get_business_data(year=2014):
    """
    :param year: The year to query the data for; defaults to 2014
    :return: Census ASE Business data as a list of JSON objects
    """

    # 2014 values for the URL and query vars
    business_url = "https://api.census.gov/data/2014/ase/cscb"

    # Shorten
    business_vars = ["ASECB", "ASECB_TTL", "EMP", "PAYANN", "YIBSZFI",
                     "YIBSZFI_TTL"]
    business_vars = ["ASECB", "ASECB_TTL", "EMP", "PAYANN"]

    # 2012 values
    if year == 2012:
        business_url = "https://api.census.gov/data/2012/sbo/cscb"
        business_vars = ["CBGROUP", "CBGROUP_TTL", "EMP", "PAYANN", "YRESTBUS",
                         "YRESTBUS_TTL"]
        # Shorten
        business_vars = ["CBGROUP", "CBGROUP_TTL", "EMP", "PAYANN"]

    api_key = "5fff67c7b4559d14fc4adc2da294f674e95c1a3e"
    return query_census(business_url, business_vars, api_key)


def get_census_var_string(census_vars):
    """
    Generates a formatted string of the variables to query for
    :param census_vars: a list of variables to join
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


def get_census_dataframe(census_data, year=2014, columns_to_drop=None):
    """
    Creates a Pandas DataFrame from the given data, removes specified columns,
    and makes sure numeric data are converted to numbers
    :param census_data: the given census data
    :param year: the year of the data
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

    # Format the DataFrame to make it have the same column names across years
    columns_to_rename = get_columns_to_rename()
    df_census = df_census.rename(columns=columns_to_rename)

    df_census = df_census.drop(columns=columns_to_drop, errors="ignore")

    # Different cases depending on which variables are in the table

    # Convert integer types that are currently treated as strings
    vars_to_convert = {
        "EMP": np.int64,
        "PAYANN": np.int64
    }
    df_census = df_census.astype(vars_to_convert)

    df_census = add_columns_to_business_df(df_census)
    return df_census


def add_columns_to_business_df(df):
    """
    Inserts additional columns into the DataFrame
    :param df:
    :return:
    """
    pay_per_emp = df["PAYANN"] / df["EMP"]
    # Add new columns via assign()
    df = df.assign(PAYPEREMP=pay_per_emp)
    return df


def main():
    path_2014 = "C:\\Users\\Andrew\\PycharmProjects\\census-ase\\business-2014.xlsx"
    path_2012 = "C:\\Users\\Andrew\\PycharmProjects\\census-ase\\business-2012.xlsx"
    multi_sheet_path = "C:\\Users\\Andrew\\PycharmProjects\\census-ase\\characteristics-of-businesses.xlsx"
    combined_path = "C:\\Users\\Andrew\\PycharmProjects\\census-ase\\combined.xlsx"
    sheet_name_2014 = "2014"
    sheet_name_2012 = "2012"
    sheet_name_combined = "2014 and 2012"

    # 2012 setup
    year = 2012
    bus_2012 = get_business_data(year)
    cols_to_drop_2012 = get_columns_to_drop(year)
    bus_2012_df = get_census_dataframe(bus_2012, year, cols_to_drop_2012)

    # 2014 setup
    year = 2014
    bus_2014 = get_business_data(year)
    cols_to_drop_2014 = get_columns_to_drop(year)
    bus_2014_df = get_census_dataframe(bus_2014, year, cols_to_drop_2014)

    # Exporting data
    dataframes_and_sheets = [(bus_2012_df, sheet_name_2012),
                             (bus_2014_df, sheet_name_2014)]
    export_dataframes_to_excel(multi_sheet_path, dataframes_and_sheets)

    # Combining data
    suffixes = ("_2014", "_2012")
    merged_df = bus_2014_df.merge(bus_2012_df, on="GROUP", suffixes=suffixes)
    merged_df.to_excel(combined_path)

    xvar_2012 = "GROUP"
    yvar_2012 = "PAYPEREMP_2012"
    plot_business_data(xvar_2012, yvar_2012, merged_df)




if __name__ == "__main__":
    main()