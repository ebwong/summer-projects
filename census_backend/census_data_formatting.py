# Includes methods for formatting the census data. Not currently used

import numpy as np


def get_columns_to_rename():
    """
    Returns a dict of the columns that should be renamed
    :return: a dict of the columns that should be renamed
    """
    columns_to_rename = {
        "ASECB": "GROUP",
        "ASECB_TTL": "GROUP_TTL",
        "CBGROUP": "GROUP",
        "CBGROUP_TTL": "GROUP_TTL",
        "YIBSZFI": "YIB",
        "YIBSZFI_TTL": "YIB_TTL",
        "YRESTBUS": "YIB",
        "YRESTBUS_TTL": "YIB_TTL"
    }
    return columns_to_rename

def get_columns_to_drop(year):
    """
    Returns a list of strings indicating which columns to drop for the data
    in the given year
    :param year: the year of the data
    :return: a list of which columns to drop for the given year; "us" is always
    dropped
    """

    cols_to_drop = ["us"] # Always drop "us"
    # cols_to_drop.append("GROUP")
    cols_to_drop.append("YIB")
    return cols_to_drop

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

