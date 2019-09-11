import pandas as pd

def export_dataframe_to_csv(df, path):
    csv_path = "C:\\Users\\Andrew\\PycharmProjects\\census-ase\\business-data.csv"
    df.to_csv(path_or_buf=csv_path)

def export_dataframes_to_excel(path, dataframes_and_sheets):
    with pd.ExcelWriter(path) as writer:
        for pair in dataframes_and_sheets:
            df = pair[0]
            sheet_name = pair[1]
            df.to_excel(writer, sheet_name)

