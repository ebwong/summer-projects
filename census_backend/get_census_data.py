"""
Main module for querying 2014 ASE data and 2012 Survey of Business Owners
"""
import os
import json

import requests
import numpy as np
import pandas as pd

VALID_YEARS = [
    2012,
    2014,
]

# 2014 variables

EMP = "EMP"  # Employee count
FIRMPDEMP = "FIRMPDEMP"  # Number of firms
PAYANN = "PAYANN"  # Annual payroll

US_GEO = "us"

# Custom variables
PAYPEREMP = "PAYPEREMP" # Pay per employee
EMPPERFIRM = "EMPPERFIRM"  # Employees per firm

# 2014 social groups
ASECB = "ASECB"
ASECB_TTL = "ASECB_TTL"

# 2012 social groups
CBGROUP = "CBGROUP"
CBGROUP_TTL = "CBGROUP_TTL"

# Variable codes
ALL_FIRMS = "0000"
ALL_FIRMS_CLASSIFIABLE = "9996"
ALL_FIRMS_NOT_CLASSIFIABLE = "9998"

# Standard column names
GROUP = "GROUP"
GROUP_TTL = "GROUP_TTL"

# Suffixes to append to column names when columns with the same name are merged
SUFFIXES = [
    "_2012",
    "_2014",
]


def get_business_data(year, independent_var, dependent_var):
    """
    :param year: The year to query the data for
    :return: Census Business data as a list of JSON objects
    """

    business_url = None
    business_vars = None
    if year == 2014:
        business_url = "https://api.census.gov/data/2014/ase/cscb"
        business_vars = [
            ASECB,
            ASECB_TTL,
        ] + [
            independent_var,
            dependent_var,
        ]
        # Ensure that "EMP" is queried for if it is needed for another category
        if dependent_var in [FIRMPDEMP, PAYANN]:
            business_vars.append(EMP)
    elif year == 2012:
        business_url = "https://api.census.gov/data/2012/sbo/cscb"
        business_vars = [
            CBGROUP,
            CBGROUP_TTL,
        ] + [
            independent_var,
            dependent_var,
        ]
    else:
        raise ValueError(f"Given year is not one of {VALID_YEARS}")

    api_key = os.environ["CENSUS_KEY"]

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

    # Format the census vars before querying
    census_var_string = get_census_var_string(census_vars)

    params = {
        "get": census_var_string,
        "for": "us:*",  # get results in the entire U.S.
        "key": api_key,
    }

    response = requests.get(url, params=params)
    if not response.ok:
        if response.status_code == 204:
            raise requests.exceptions.HTTPError("Query didn't return anything")
        else:
            raise requests.exceptions.HTTPError(response.text)
    return response.json()


def get_census_dataframe(year, census_data, independent_var, dependent_var):
    """
    Creates a Pandas DataFrame from the given data, removes specified columns,
    and makes sure numeric data are converted to numbers
    :param year: the year of the data
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

    # Format the DataFrame to make it have the same column names across years
    columns_to_rename = None
    if year == 2014:
        columns_to_rename = {
            ASECB: GROUP,
            ASECB_TTL: GROUP_TTL,
        }
    elif year == 2012:
        columns_to_rename = {
            CBGROUP: GROUP,
            CBGROUP_TTL: GROUP_TTL,
        }
    df_census = df_census.rename(columns=columns_to_rename)



    # Convert integer types that are currently treated as strings
    vars_to_convert = {}
    # Verify that a column exists for the variable
    # before trying to convert the type
    if EMP in df_census.columns:
        vars_to_convert[EMP] = np.int64
    if PAYANN in df_census.columns:
        vars_to_convert[PAYANN] = np.int64
    if FIRMPDEMP in df_census.columns:
        vars_to_convert[FIRMPDEMP] = np.int64
    # Convert the column types
    df_census = df_census.astype(vars_to_convert)

    # Drop rows that include aggregate groups because the values are too large
    # and disrupt the plotting

    df_census = df_census[(df_census[GROUP] != ALL_FIRMS) &
                          (df_census[GROUP] != ALL_FIRMS_CLASSIFIABLE) &
                          (df_census[GROUP] != ALL_FIRMS_NOT_CLASSIFIABLE)
                          ]

    # Add in custom columns that better summarize the data
    df_census = add_columns_to_business_df(df_census)

    # Drop unwanted columns or columns whose values are too large to easily plot
    columns_to_drop = [
        FIRMPDEMP,
        PAYANN,
        US_GEO,
    ]

    # If EMP is not one of the variables to graphed but it is in the
    # table, remove it
    if EMP not in [independent_var, dependent_var] and EMP in df_census.columns:
        columns_to_drop.append(EMP)

    df_census = df_census.drop(columns=columns_to_drop, errors="ignore")

    return df_census


def add_columns_to_business_df(df):
    """
    Inserts additional columns into the DataFrame
    :param df:
    :return:
    """
    if PAYANN in df.columns:
        pay_per_emp = df[PAYANN] / df[EMP]
        # Add new columns via assign()
        df = df.assign(PAYPEREMP=pay_per_emp)
    if FIRMPDEMP in df.columns:
        emp_per_firm = df[EMP] / df[FIRMPDEMP]
        df = df.assign(EMPPERFIRM=emp_per_firm)
    return df


def get_census_data(independent_var, dependent_var):
    """
    Returns a dict containing the data for the requested variables in a table format
    :param census_vars: the chosen variable
    :return:
    """

    # Adjust the names of the variables for querying
    if dependent_var == PAYPEREMP:
        dependent_var = PAYANN
    elif dependent_var == EMPPERFIRM:
        dependent_var = FIRMPDEMP

    year_2014 = 2014
    bus_2014 = get_business_data(year_2014, independent_var, dependent_var)
    # print(bus_2014)
    df_bus_2014 = get_census_dataframe(year_2014, bus_2014, independent_var, dependent_var)
    print(df_bus_2014)

    """
    Fix 2012 code once done with 2014
    year_2012 = 2012
    bus_2012 = get_business_data(year_2012, list(census_vars))
    df_bus_2012 = get_census_dataframe(bus_2012, year_2012)
     # Combine the data
    merged_df = df_bus_2014.merge(df_bus_2012, on="GROUP", suffixes=suffixes)
    """

    return df_bus_2014.to_json()

if __name__ == "__main__":
    independent_var = "YIBSZFI"
    dependent_var = PAYPEREMP
    get_census_data(independent_var, dependent_var)

    """
        with open(
            "C:\\Users\\Andrew\\Desktop\\summer-projects\\census_backend\\react.txt",
            "w+") as f:
        f.write(str(census_vars))
    """



