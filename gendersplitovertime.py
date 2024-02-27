import pandas as pd
import numpy as np

file_paths = [
    r'C:\Users\19736\OneDrive\Documents\Github\CMS_2013_USA.csv',
    r'C:\Users\19736\OneDrive\Documents\Github\CMS_2014_USA.csv',
    r'C:\Users\19736\OneDrive\Documents\Github\CMS_2015_USA.csv',
    r'C:\Users\19736\OneDrive\Documents\Github\CMS_2016_USA.csv',
    r'C:\Users\19736\OneDrive\Documents\Github\CMS_2017_USA.csv',
    r'C:\Users\19736\OneDrive\Documents\Github\CMS_2018_USA.csv',
    r'C:\Users\19736\OneDrive\Documents\Github\CMS_2019_USA.csv',
    r'C:\Users\19736\OneDrive\Documents\Github\CMS_2020_USA.csv',
    r'C:\Users\19736\OneDrive\Documents\Github\CMS_2021_USA.csv'
]

dataframes = []

for file_path in file_paths:
    year = int(file_path.split('_')[1].split('.')[0])
    df = pd.read_csv(file_path)
    df['year'] = year
    dataframes.append(df)

combined_df = pd.concat(dataframes)

number_of_physicians = combined_df.groupby('year')['Rndrng_NPI'].nunique()

Male = combined_df[combined_df['Rndrng_Prvdr_Gndr'] == 'M']
Female = combined_df[combined_df['Rndrng_Prvdr_Gndr'] == 'F']

male_unique_npi_per_year = Male.groupby('year')['Rndrng_NPI'].nunique()
female_unique_npi_per_year = Female.groupby('year')['Rndrng_NPI'].nunique()

print("Number of unique Rndrng_NPI in Male per year:")
print(male_unique_npi_per_year)

print("Number of unique Rndrng_NPI in Female per year:")
print(female_unique_npi_per_year)

import matplotlib.pyplot as plt


plt.xlabel('Year')
plt.ylabel('Number of Dermatologists')
plt.title('Number of U.S. Medicare Dermatologists by Gender over Time')
plt.plot(male_unique_npi_per_year.index, male_unique_npi_per_year.values, color='lightskyblue', label='Male')
plt.plot(female_unique_npi_per_year.index, female_unique_npi_per_year.values, color='steelblue', label='Female')
plt.legend()

plt.show()

# Filter the combined_df for the year 2013
df_2013 = combined_df[combined_df['year'] == 2013]

# Count the number of male and female physicians in 2013
male_count_2013 = df_2013[df_2013['Rndrng_Prvdr_Gndr'] == 'M']['Rndrng_NPI'].nunique()
female_count_2013 = df_2013[df_2013['Rndrng_Prvdr_Gndr'] == 'F']['Rndrng_NPI'].nunique()

# Create a pie chart for 2013
labels_2013 = ['Male', 'Female']
sizes_2013 = [male_count_2013, female_count_2013]
colors_2013 = ['lightskyblue', 'steelblue']

plt.subplot(1, 2, 1)
plt.pie(sizes_2013, labels=labels_2013, colors=colors_2013, autopct='%1.1f%%', wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
plt.title('Distribution of Male and Female Dermatologists in 2013')

# Filter the combined_df for the year 2021
df_2021 = combined_df[combined_df['year'] == 2021]

# Count the number of male and female physicians in 2021
male_count_2021 = df_2021[df_2021['Rndrng_Prvdr_Gndr'] == 'M']['Rndrng_NPI'].nunique()
female_count_2021 = df_2021[df_2021['Rndrng_Prvdr_Gndr'] == 'F']['Rndrng_NPI'].nunique()

# Create a pie chart for 2021
labels_2021 = ['Male', 'Female']
sizes_2021 = [male_count_2021, female_count_2021]
colors_2021 = ['lightskyblue', 'steelblue']

plt.subplot(1, 2, 2)
plt.pie(sizes_2021, labels=labels_2021, colors=colors_2021, autopct='%1.1f%%', wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
plt.title('Distribution of Male and Female Dermatologists in 2021')

plt.show()

total_physicians_over_time = number_of_physicians.values

plt.xlabel('Year')
plt.ylabel('Number of Dermatologists')
plt.title('Total Number of Physicians over Time')
plt.plot(number_of_physicians.index, total_physicians_over_time, color='darkblue')
plt.show()

unique_npi_per_state = combined_df.groupby('Rndrng_Prvdr_State_Abrvtn')['Rndrng_NPI'].nunique()
print("Number of unique Rndrng_NPI per state:")
unique_npi_per_state = unique_npi_per_state[~unique_npi_per_state.index.isin(['AE', 'AP', 'DC', 'GU', 'PR', 'VI', 'XX', 'ZZ'])]
print(unique_npi_per_state)

# Sort the unique_npi_per_state in ascending order
sorted_unique_npi_per_state = unique_npi_per_state.sort_values()

# Get the 5 states with the lowest number of unique_npi_per_state
lowest_states = sorted_unique_npi_per_state.head(5)

# Get the 5 states with the highest number of unique_npi_per_state
highest_states = sorted_unique_npi_per_state.tail(5)

# Create a bar chart for the states with the lowest number of unique_npi_per_state
plt.figure()
plt.xlabel('State')
plt.ylabel('Number of Unique Rndrng_NPI')
plt.title('States with the Lowest Number of Dermatologists')
lowest_states.plot(kind='bar', color='lightskyblig')
plt.show()

# Create a bar chart for the states with the highest number of unique_npi_per_state
plt.figure()
plt.xlabel('State')
plt.ylabel('Number of Unique Rndrng_NPI')
plt.title('States with the Highest Number of Dermatologists')
highest_states.plot(kind='bar', color='lightskyblue')
plt.show()

