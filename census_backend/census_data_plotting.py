# Plots the census data using matplotlib. Not currently used
import matplotlib.pyplot as plt
from cycler import cycler


def plot_business_data(xvar, yvar, df):
    """
    Plots the data from the given DataFrame
    :param xvar: the variable to plot on the x-axis
    :param yvar: the variable to plot on the y-axis
    :param df: the given DataFrame
    :return: a path to a saved image file of the graph
    """

    demographic_category_key = "GROUP"
    xlabel = xvar
    ylabel= yvar

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
        "#000000", # black
    ]
    my_cycle = cycler(color=colors)
    ax.set_prop_cycle(my_cycle)

    # Get a list of all of the demographic categories
    demographic_categories = df[demographic_category_key].unique()

    for category in demographic_categories:
        # Get a DataFrame that belongs to this category
        cat_df = df[df[demographic_category_key] == category]
        # Plot this category's data
        ax.plot(cat_df[xvar].values, cat_df[yvar].values, marker, label=category + " 2012")
        # This way doesn't cycle colors with markers
        # ax.plot(cat_df["EMP_2014"].values, cat_df["PAYANN_2014"].values, "^", label=category + " 2014")

    for category in demographic_categories:
        # Get a DataFrame that belongs to this category
        cat_df = df[df[demographic_category_key] == category]
        # Plot this category's data
        ax.plot(cat_df["GROUP"].values, cat_df["PAYPEREMP_2014"].values, "^", label=category + " 2014")



    ax.legend(loc="lower right", prop={"size": 6})
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(f"{xlabel} vs {ylabel}")

    # plt.show()

    save_path = "C:\\Users\\Andrew\\Desktop\\census_web_img.png"
    plt.savefig(save_path)
    return save_path