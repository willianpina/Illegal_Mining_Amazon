#####################
# Import Lybraries  #
#####################

import pandas as pd
from IPython.display import display

METADATA = "https://zenodo.org/records/6810792/files/metadata.csv?download=1"

# Read metadata
metadata = pd.read_csv(METADATA)


# Run
if __name__ == "__main__":
    # Print the first 5 rows of metadata
    display(metadata.head())






