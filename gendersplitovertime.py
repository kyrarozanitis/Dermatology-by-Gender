import pandas as pd

file_paths = [
    r'C:\Users\19736\OneDrive\Documents\Github\CMS_2021_USA.csv',
    r'C:\Users\19736\OneDrive\Documents\Github\CMS_2021_UK.csv',
    r'C:\Users\19736\OneDrive\Documents\Github\CMS_2021_AUS.csv'
]

data = pd.DataFrame()  # Create an empty DataFrame to store the combined data

for file_path in file_paths:
    df = pd.read_csv(file_path)  # Read each file
    data = data.append(df)  # Append the data to the combined DataFrame

# Now you can work with the combined data
# ...