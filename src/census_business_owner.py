"""
Includes methods for working with Business Owners
"""
def get_owner_data():
    """
    Returns Census ASE Business Owner data
    :return:
    """

    owner_url = "https://api.census.gov/data/2014/ase/cscbo"
    owner_vars = ("ASECBO", "ASECBO_TTL", "OWNPDEMP", "USBORNCIT")  # The variables to query for
    api_key = "5fff67c7b4559d14fc4adc2da294f674e95c1a3e"
    return query_census(owner_url, owner_vars, api_key)

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