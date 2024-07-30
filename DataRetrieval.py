import pandas as pd
import numpy as np
from io import BytesIO
import requests
import zipfile
import os

# This entire program runs on the assumption that all years picked are consecutive

year_start = 2019
year_end = 2022
# If wanting to include year 2023 and year_end above is 2022, set below to "True"
include_2023 = True
# At time of publishing, lastest annual data file is 2022, but like many other years, it contains a chunk of datapoints for the next year
# There are enough datapoints of 2023 in the 2022 file to properly run statistical tests on it

columns_num_to_keep_2019 = ['0', '5', '72', '73', '267', '271', '276', '283']
columns_num_to_keep_2020 = ['0', '5', '66', '68', '236', '240', '245', '252']
columns_num_to_keep_2021 = ['0', '5', '73', '75', '256', '260', '265', '272']
columns_num_to_keep_2022 = ['0', '5', '66', '68', '281', '285', '290', '297']

column_renames_2019 = {"0" : "state", "5" : "year", "72" : "income", "73" : "weight (Ib)", "267" : "race", "271" : "sex", "276" : "height (in)", "283" : "education"}
column_renames_2020 = {"0" : "state", "5" : "year", "66" : "income", "68" : "weight (Ib)", "236" : "race", "240" : "sex", "245" : "height (in)", "252" : "education"}
column_renames_2021 = {"0" : "state", "5" : "year", "73" : "income", "75" : "weight (Ib)", "256" : "race", "260" : "sex", "265" : "height (in)", "272" : "education"}
column_renames_2022 = {"0" : "state", "5" : "year", "66" : "income", "68" : "weight (Ib)", "281" : "race", "285" : "sex", "290" : "height (in)", "297" : "education"}

num_of_variables_2019 = 342
num_of_variables_2020 = 279
num_of_variables_2021 = 303
num_of_variables_2022 = 328

# URL to download the Excel file of unemployment (UE) data of states by year
UE_url = "https://dlt.ri.gov/media/15101/download?language=en"

states_dict = {
    "Alabama": 1.0,
    "Alaska": 2.0,
    "Arizona": 4.0,
    "Arkansas": 5.0,
    "California": 6.0,
    "Colorado": 8.0,
    "Connecticut": 9.0,
    "Delaware": 10.0,
    "District of Columbia": 11.0,
    "Florida": 12.0,
    "Georgia": 13.0,
    "Hawaii": 15.0,
    "Idaho": 16.0,
    "Illinois": 17.0,
    "Indiana": 18.0,
    "Iowa": 19.0,
    "Kansas": 20.0,
    "Kentucky": 21.0,
    "Louisiana": 22.0,
    "Maine": 23.0,
    "Maryland": 24.0,
    "Massachusetts": 25.0,
    "Michigan": 26.0,
    "Minnesota": 27.0,
    "Mississippi": 28.0,
    "Missouri": 29.0,
    "Montana": 30.0,
    "Nebraska": 31.0,
    "Nevada": 32.0,
    "New Hampshire": 33.0,
    "New Mexico": 35.0,
    "New York": 36.0,
    "North Carolina": 37.0,
    "North Dakota": 38.0,
    "Ohio": 39.0,
    "Oklahoma": 40.0,
    "Oregon": 41.0,
    "Pennsylvania": 42.0,
    "Rhode Island": 44.0,
    "South Carolina": 45.0,
    "South Dakota": 46.0,
    "Tennessee": 47.0,
    "Texas": 48.0,
    "Utah": 49.0,
    "Vermont": 50.0,
    "Virginia": 51.0,
    "Washington": 53.0,
    "West Virginia": 54.0,
    "Wisconsin": 55.0,
    "Wyoming": 56.0
}

year_list = []
for i in range(year_start, year_end + 1):
    year_list.append(str(i))
if include_2023 == True:
    year_list.append("2023")
year_list.reverse()

# DCV = Dynamically-Created-Variables
# The purpose of DCV is just so no issues are shown by VSCode and makes the program look cleaner (as well as avoid confusion)
DCV = {}

# SCV = Statically-Created-Variables
# The purpose of putting these in a dictionary is so that later on all the years can be automatically ran in the get_yearly_data loop without manually typing out each year
SCV = {}

columns_num_to_keep_2019 = ['0', '5', '72', '73', '267', '271', '276', '283']
columns_num_to_keep_2020 = ['0', '5', '66', '68', '236', '240', '245', '252']
columns_num_to_keep_2021 = ['0', '5', '73', '75', '256', '260', '265', '272']
columns_num_to_keep_2022 = ['0', '5', '66', '68', '281', '285', '290', '297']

column_renames_2019 = {"0" : "state", "5" : "year", "72" : "income", "73" : "weight (Ib)", "267" : "race", "271" : "sex", "276" : "height (in)", "283" : "education"}
column_renames_2020 = {"0" : "state", "5" : "year", "66" : "income", "68" : "weight (Ib)", "236" : "race", "240" : "sex", "245" : "height (in)", "252" : "education"}
column_renames_2021 = {"0" : "state", "5" : "year", "73" : "income", "75" : "weight (Ib)", "256" : "race", "260" : "sex", "265" : "height (in)", "272" : "education"}
column_renames_2022 = {"0" : "state", "5" : "year", "66" : "income", "68" : "weight (Ib)", "281" : "race", "285" : "sex", "290" : "height (in)", "297" : "education"}

num_of_variables_2019 = 342
num_of_variables_2020 = 279
num_of_variables_2021 = 303
num_of_variables_2022 = 328

def create_year_and_url_variables(start, end):
    for year in range(start, end + 1):
        DCV[f'y{year}'] = year
        DCV[f'url_{year}'] = f"https://www.cdc.gov/brfss/annual_data/{year}/files/LLCP{year}XPT.zip"
        SCV[f"columns_num_to_keep_{year}"] = globals()[f"columns_num_to_keep_{year}"]
        SCV[f"column_renames_{year}"] = globals()[f"column_renames_{year}"]
        SCV[f"num_of_variables_{year}"] = globals()[f"num_of_variables_{year}"]
    # Potentially will add part for 2010 and below years (which have a different url format)

def get_yearly_data(url_year, columns_num_to_keep_year, column_renames_year, N, y):
    
    if os.path.exists(f"Reconstructed{y}Dataset.csv"):
        print(f"Reconstructed{y}Dataset.csv already exists.")
    elif os.path.exists("DatasetForLinearRegressionsOnBMI.csv"):
        print("DatasetForLinearRegressionsOnBMI.csv already exists.")    
    else:

        # Download the ZIP file
        response = requests.get(url_year)
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            # Assuming there's only one file in the ZIP (you might need to adjust this)
            file_name = z.namelist()[0]
            with z.open(file_name) as f:
                # Read the data into a Pandas DataFrame
                df = pd.read_sas(f, format="xport")

        # Convert DataFrame to numpy array
        numpy_array = df.to_numpy()

        # Make numpy array 1D
        flattened_array = numpy_array.flatten()

        # Calculate the number of rows and reshape the array
        num_columns = N
        num_rows = len(flattened_array) // num_columns

        # Ensure the flattened array can be evenly divided into rows of N columns, if not, drop any remaining datapoints
        # Note: Potentially dropping an unfinished row of data will not affect the results noticeably, as there are hundred of thousands of datapoints
        if len(flattened_array) % num_columns != 0:
            drop_remainder = len(flattened_array) % num_columns
            flattened_array = flattened_array[:-drop_remainder]

        # Reshape the flattened array into the correct shape
        reshaped_array = flattened_array.reshape(num_rows, num_columns)

        # Convert the reshaped array back to a DataFrame
        reconstructed_df = pd.DataFrame(reshaped_array)

        # Verify the shape of the DataFrame
        assert reconstructed_df.shape == (num_rows, num_columns), f"Unexpected DataFrame shape: {reconstructed_df.shape}"

        # Save the reconstructed DataFrame to a new file
        reconstructed_df.to_csv(f'Reconstructed{y}Dataset.csv', index=False)

        print(f"Reconstructed data for year {y} saved successfully.")

        df = pd.read_csv(f"Reconstructed{y}Dataset.csv")
        #  These are the columns rows we want
        df = df[columns_num_to_keep_year]
        # Cleans the second column up a bit to appear cleaner
        df['5'] = df['5'].str.strip("b'")
        # This gives the proper names to the columns we kept
        df = df.rename(columns=column_renames_year)
        # Save the filtered DataFrame to the same file, replacing the old dataset

        # This code cleans up the data by removing any rows with NaN and any values that represent groups such as "Refused to answer" or "No response" 
        # df = df[df["state"] < 60]
        df = df[df["education"] != 9.0]
        df = df[df["income"] < 13.0]
        df = df[df["race"] != 9.0]
        # I remove any values of weight above 999 because some values in kilograms are indicated by an initial 9 (i.e. 9068) and groups such as "Don't Know" and "Refused" are above 999
        df = df[df["weight (Ib)"] < 999.0]
        df = df[df["state"] < 60]
        df = df.dropna()

        # Create the BMI row
        df["BMI"] = ((df["weight (Ib)"] * 703) / (df["height (in)"] ** 2)).round(5)

        df.to_csv(f'Reconstructed{y}Dataset.csv', index=False)
        print(f"Data for year {y} cleaned successfully.")

# This function assumes all years are consecutive
def concatenate_and_delete_files(year_start, number_of_years):
    if os.path.exists(f"Reconstructed{year_start}Dataset.csv"):    
        # Read the first file (first year)
        df_combined = pd.read_csv(f"Reconstructed{year_start}Dataset.csv")
        # Loop through the other files, first reading them and then concatenating them
        for i in range(1, number_of_years):
            df_copy = pd.read_csv(f"Reconstructed{year_start + i}Dataset.csv")
            df_combined = pd.concat([df_combined, df_copy], ignore_index=True)
        df_combined.to_csv("DatasetForLinearRegressionsOnBMI.csv", index=False)
        # Delete the old files
        for i in range(number_of_years):
            os.remove(f"Reconstructed{year_start + i}Dataset.csv")
    else:
        print("Did not find dataset of first year to commence the concatenate_and_delete_files() function.")

# If the file exists, skip everything below
if os.path.exists("UnemploymentData.csv"):
    print("UnemploymentData.csv already exists.")
else:

    # Download the Excel file
    response = requests.get(UE_url)
    with open('UnemploymentData.xlsx', 'wb') as file:
        file.write(response.content)

    # Read the downloaded Excel file
    df = pd.read_excel('UnemploymentData.xlsx')
    df = df[7:]

    # Save the DataFrame as a CSV file
    df.to_csv('UnemploymentData.csv', index=False)
    os.remove("UnemploymentData.xlsx")

    # About 38 columns in the excel file
    # Select all the columns that are actually yearly data
    x = []
    for i in range(38):
        if (i - 1) % 3 == 0:
            x.append(f"Unnamed: {i}")

    # Set the columns to keep in a variable and drop all other variables
    # Note: We add in X so that if reran, it doesn't cause issues
    columns_to_keep = set(x + year_list + ["Unemployment Rates for States"])
    df = df.iloc[:, df.columns.isin(columns_to_keep)]

    # Ensure X has the correct length and your df has the appropriate number of columns to be modified.
    # This assumes the columns you want to modify are in a continuous range starting from the second column.
    if len(year_list) <= len(df.columns) - 1:
        df.columns = [df.columns[0]] + [f"{year_list[i]}" if i < len(year_list) else col for i, col in enumerate(df.columns[1:])]
    else:
        raise ValueError("Length of X exceeds the number of columns available for renaming.")

    # Drop all columns that contain "Unnamed" as we don't want them for our data
    phrase = "Unnamed: "
    columns_to_drop = df.filter(regex=phrase).columns
    df = df.drop(columns=columns_to_drop)

    df = df.rename(columns={"Unemployment Rates for States" : "state"})
    df = pd.melt(df, id_vars=["state"], var_name="year", value_name="unemployment rate")

    # Map the state names to the state codes, doing this now will help later
    df["state_code"] = df["state"].map(states_dict)

    df.to_csv("UnemploymentData.csv", index=False)

create_year_and_url_variables(year_start, year_end)

for year in range(year_start, year_end  + 1):
    dataset_for_year = get_yearly_data(DCV[f"url_{year}"], SCV[f"columns_num_to_keep_{year}"], SCV[f"column_renames_{year}"], SCV[f"num_of_variables_{year}"], DCV[f"y{year}"])

concatenate_and_delete_files(year_start, (year_end - year_start + 1))

print("Cool")