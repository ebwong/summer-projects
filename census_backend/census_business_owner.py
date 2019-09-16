# Contains methods for working with Business Owners, in contrast to
# Businesses. Because some API variables are different, the Business Owners
# have been separated from the Businesses. Currently, the project does not
# work with Business owners

def get_owner_data():
    """
    Returns Census ASE Business Owner data
    :return:
    """
    owner_url = "https://api.census.gov/data/2014/ase/cscbo"


