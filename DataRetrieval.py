import pandas as pd
import numpy as np
from io import BytesIO
import requests
import zipfile
import os

# Note: For the year 2022, it also has some data for the year 2023

url_2019 = "https://www.cdc.gov/brfss/annual_data/2019/files/LLCP2019XPT.zip"
url_2020 = "https://www.cdc.gov/brfss/annual_data/2020/files/LLCP2020XPT.zip"
url_2021 = "https://www.cdc.gov/brfss/annual_data/2021/files/LLCP2021XPT.zip"
url_2022_2023 = "https://www.cdc.gov/brfss/annual_data/2022/files/LLCP2022XPT.zip"

columns_num_to_keep_2019 = ['0', '5', '72', '73', '267', '271', '276', '283']
columns_num_to_keep_2020 = ['0', '5', '66', '68', '236', '240', '245', '252']
columns_num_to_keep_2021 = ['0', '5', '73', '75', '256', '260', '265', '272']
columns_num_to_keep_2022_2023 = ['0', '5', '66', '68', '281', '285', '290', '297']

column_renames_2019 = {"0" : "state", "5" : "year", "72" : "income", "73" : "weight (Ib)", "267" : "race", "271" : "sex", "276" : "height (in)", "283" : "education"}
column_renames_2020 = {"0" : "state", "5" : "year", "66" : "income", "68" : "weight (Ib)", "236" : "race", "240" : "sex", "245" : "height (in)", "252" : "education"}
column_renames_2021 = {"0" : "state", "5" : "year", "73" : "income", "75" : "weight (Ib)", "256" : "race", "260" : "sex", "265" : "height (in)", "272" : "education"}
column_renames_2022_2023 = {"0" : "state", "5" : "year", "66" : "income", "68" : "weight (Ib)", "281" : "race", "285" : "sex", "290" : "height (in)", "297" : "education"}

num_of_variables_2019 = 342
num_of_variables_2020 = 279
num_of_variables_2021 = 303
num_of_variables_2022_2023 = 328

y1 = "2019"
y2 = "2020"
y3 = "2021"
y4 = "2022"

def get_yearly_data(url_year, columns_num_to_keep_year, column_renames_year, N, y):
    
    if os.path.exists(f"Reconstructed{y}Dataset.csv"):
        print(f"Reconstructed{y}Dataset.csv already exists.")
    elif os.path.exists(f"DatasetForLinearRegressionsOnBMI.csv"):
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
        print("Filtered DataFrame columns: ", df.columns)
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

dataset_for_2019 = get_yearly_data(url_2019, columns_num_to_keep_2019, column_renames_2019, num_of_variables_2019, y1)

dataset_for_2020 = get_yearly_data(url_2020, columns_num_to_keep_2020, column_renames_2020, num_of_variables_2020, y2)

dataset_for_2021 = get_yearly_data(url_2021, columns_num_to_keep_2021, column_renames_2021, num_of_variables_2021, y3)

dataset_for_2022_2023 = get_yearly_data(url_2022_2023, columns_num_to_keep_2022_2023, column_renames_2022_2023, num_of_variables_2022_2023, y4)

concatenate_and_delete_files(2019, 4)

print("Cool")




