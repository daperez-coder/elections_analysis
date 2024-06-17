import os
import requests
import pandas as pd

def fetch_data():
    """
    Downloads election data and saves it as XLSX files in a 'downloaded-files' folder.
    """
    # Define the URLs and filenames for the election data
    urls = [
        "https://www.data.gouv.fr/fr/datasets/r/f0b85156-91c2-4c8a-9b3f-beda48d15ecd",
        "https://www.data.gouv.fr/fr/datasets/r/1996b2bc-e95a-4481-904f-28d16987fe61",
        "https://www.data.gouv.fr/fr/datasets/r/d6d0e0c4-ff00-43bf-a0c9-c195b71f223a",
        "https://www.data.gouv.fr/fr/datasets/r/3a26bbf8-4288-4e84-b765-52e5b446de4c",
        "https://www.data.gouv.fr/fr/datasets/r/98eb9dab-f328-4dee-ac08-ac17211357a8",
        "https://www.data.gouv.fr/fr/datasets/r/92fcc5b6-df2a-4a33-ab28-555803511206"
    ]
    filenames = [
        "européennes_2019_t1.xlsx",
        "européennes_2024_t1.xlsx",
        "législatives_2022_t1.xlsx",
        "législatives_2022_t2.xlsx",
        "présidentielles_2022_t1.xlsx",
        "présidentielles_2022_t2.xlsx"
    ]
    election_names = [
        "européennes_2019_t1",
        "européennes_2024_t1",
        "législatives_2022_t1",
        "législatives_2022_t2",
        "présidentielles_2022_t1",
        "présidentielles_2022_t2"
    ]

    # Create the 'downloaded-files' folder if it doesn't exist
    if not os.path.exists("downloaded-files"):
        os.makedirs("downloaded-files")

    # Download and save the election data as XLSX files
    for url, filename, election_name in zip(urls, filenames, election_names):
        response = requests.get(url)
        with open(os.path.join("downloaded-files", filename), "wb") as f:
            f.write(response.content)
        print(f"Downloaded {election_name} data and saved as {filename}")

def store_as_parquet(folder="downloaded-files"):
    """
    Loads the XLSX files in the 'downloaded-files' folder, converts them to Pandas DataFrames, and saves them as Parquet files.
    """
    filenames = [
        "européennes_2019_t1.xlsx",
        "européennes_2024_t1.xlsx",
        "législatives_2022_t1.xlsx",
        "législatives_2022_t2.xlsx",
        "présidentielles_2022_t1.xlsx",
        "présidentielles_2022_t2.xlsx"
    ]
    for filename in filenames:
        df = pd.read_excel(os.path.join(folder, filename))
        parquet_filename = os.path.splitext(filename)[0] + ".parquet"
        df.to_parquet(os.path.join(folder, parquet_filename))
        print(f"Saved {parquet_filename} to {folder}")

def store_as_pickle(folder="downloaded-files"):
    """
    Loads the XLSX files in the 'downloaded-files' folder, converts them to Pandas DataFrames, and saves them as Pickle files.
    """
    filenames = [
        "européennes_2019_t1.xlsx",
        "européennes_2024_t1.xlsx",
        "législatives_2022_t1.xlsx",
        "législatives_2022_t2.xlsx",
        "présidentielles_2022_t1.xlsx",
        "présidentielles_2022_t2.xlsx"
    ]
    for filename in filenames:
        df = pd.read_excel(os.path.join(folder, filename))
        pickle_filename = os.path.splitext(filename)[0] + ".pkl"
        df.to_pickle(os.path.join(folder, pickle_filename))
        print(f"Saved {pickle_filename} to {folder}")
