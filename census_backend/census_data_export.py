# Includes convenience methods for exporting a DataFrame to a CSV file or
# Excel file
import pandas as pd


def export_dataframe_to_csv(df, csv_path):
    """
    Saves the given DataFrame's data to the given path
    :param df: the given DataFrame
    :param path: path to file
    :return: None
    """
    df.to_csv(path_or_buf=csv_path)

def export_dataframes_to_excel(path, dataframes_and_sheets):
    """
    Saves the given DataFrame's data to the given path
    :param path: the path to the file
    :param dataframes_and_sheets: a tuple of DataFrames and sheet names to
    save the data as
    :return: None
    """
    with pd.ExcelWriter(path) as writer:
        for pair in dataframes_and_sheets:
            df = pair[0]
            sheet_name = pair[1]
            df.to_excel(writer, sheet_name)

