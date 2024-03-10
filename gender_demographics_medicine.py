import pandas as pd
import numpy as np
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import os

def extract_data(folder_path):
    # Define the file paths
    # Get the list of files in the folder
    files = os.listdir(folder_path)

    # Filter the files to only include CSV files
    csv_files = [file for file in files if file.endswith('.csv')]

    # Create the list of file paths
    file_paths = [os.path.join(folder_path, file) for file in csv_files]

    # Create an empty list to store the dataframes
    dataframes = []

    # Read each CSV file, add the year as a column, and append the dataframe to the list
    for file_path in file_paths:
        year = int(file_path.split('_')[1].split('.')[0])
        df = pd.read_csv(file_path)
        df['year'] = year
        dataframes.append(df)

    # Combine all the dataframes into a single dataframe
    combined_df = pd.concat(dataframes)
    return combined_df

def sort_data_by_gender(data):
    # Calculate the number of unique physicians per year
    number_of_physicians = data.groupby('year')['Rndrng_NPI'].nunique()

    # Filter the data for male and female physicians
    Male = data[data['Rndrng_Prvdr_Gndr'] == 'M']
    Female = data[data['Rndrng_Prvdr_Gndr'] == 'F']

    # Calculate the number of unique physicians per year for male and female physicians using NPI
    male_unique_npi_per_year = Male.groupby('year')['Rndrng_NPI'].nunique()
    female_unique_npi_per_year = Female.groupby('year')['Rndrng_NPI'].nunique()

    # Print the number of unique male physicians per year
    print("Number of unique Rndrng_NPI in Male per year:")
    print(male_unique_npi_per_year)

    # Print the number of unique female physicians per year
    print("Number of unique Rndrng_NPI in Female per year:")
    print(female_unique_npi_per_year)
    return male_unique_npi_per_year, female_unique_npi_per_year, number_of_physicians

# Create line graph of the number of physicians by gender over time
def create_gender_comp_line_graph(male_unique_npi_per_year, female_unique_npi_per_year):
    plt.xlabel('Year')
    plt.ylabel('Number of Physicians')
    plt.title('Number of U.S. Medicare Dermatologists by Gender by Year')

    plt.plot(male_unique_npi_per_year.index, male_unique_npi_per_year.values, color='lightskyblue', label='Male')
    plt.plot(female_unique_npi_per_year.index, female_unique_npi_per_year.values, color='steelblue', label='Female')

    plt.legend()

    # Calculate and print the slope of the Male line
    male_slope, _ = np.polyfit(male_unique_npi_per_year.index, male_unique_npi_per_year.values, 1)
    print("Slope of Male line:", male_slope)

    # Calculate and print the slope of the Female line
    female_slope, _ = np.polyfit(female_unique_npi_per_year.index, female_unique_npi_per_year.values, 1)
    print("Slope of Female line:", female_slope)

    # Extend the y-axis to a minimum value of 4600
    plt.ylim(4600, plt.ylim()[1])
    plt.show()

def filter_data_by_year(data, year):
    # Filter the data for a specific year
    data_year = data[data['year'] == year]
    
    # Return the filtered data
    return data_year

# Create two pie charts comparing the percentage male/female physicians in 2013 and 2021
def create_pie_charts(data):
    
    # Filter the combined_df for the year 2013
    df_2013 = data[data['year'] == 2013]

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

    # Filter the data for the year 2021
    df_2021 = data[data['year'] == 2021]

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

    # Show both pie charts
    plt.show()

# Create line graph of the total number of physicians from 2013 to 2021
def create_line_graph_total_physicians(number_of_physicians):
    # Calculate the total number of physicians over time
    total = number_of_physicians.values

    # Create a line graph to visualize the total number of physicians by year
    plt.xlabel('Year')
    plt.ylabel('Number of Physicians')
    plt.title('Figure 1. Total Number of U.S. Medicare Dermatologists by Year')
    plt.plot(number_of_physicians.index, total, color='darkblue')
    plt.show()

# Create stacked barchart of states with highest and lowest percent female physicians
def create_stacked_barchart(combined_df):
    # Calculate the number of unique physicians by gender
    unique_npi_per_gender = combined_df.groupby('Rndrng_Prvdr_Gndr')['Rndrng_NPI'].nunique()

    # Print the number of unique physicians by gender
    print("Number of unique Rndrng_NPI by gender:")
    print(unique_npi_per_gender)

    # Filter the data for male and female physicians
    Male = combined_df[combined_df['Rndrng_Prvdr_Gndr'] == 'M']
    Female = combined_df[combined_df['Rndrng_Prvdr_Gndr'] == 'F']

    # Remove specified state codes
    state_codes_to_remove = ['GU', 'VI', 'DC', 'AE', 'AF', 'AP', 'XX', 'ZZ']
    Male = Male[~Male['Rndrng_Prvdr_State_Abrvtn'].isin(state_codes_to_remove)]
    Female = Female[~Female['Rndrng_Prvdr_State_Abrvtn'].isin(state_codes_to_remove)]

    # Find the number of male and female physicians by state
    males_by_state = Male.groupby('Rndrng_Prvdr_State_Abrvtn')['Rndrng_NPI'].count()
    females_by_state = Female.groupby('Rndrng_Prvdr_State_Abrvtn')['Rndrng_NPI'].count()

    # Define file path for census data csv file
    census_df = pd.read_csv('C:/Users/19736/OneDrive/Documents/Github/Census2020-2022.csv')

    # Filter the census data for the state and population columns
    census_df = census_df[['NAME', 'POPESTIMATE2021']]
    census_df = census_df.rename(columns={'NAME': 'State', 'POPESTIMATE2021': 'Population in 2021'})

    state_abbreviations = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'
    }

    # Map the state names to their abbreviations
    census_df['State'] = census_df['State'].map(state_abbreviations)
    census_df = census_df.dropna(subset=['State'])

    # Find the number of female physicians per 100,000 people by state
    merged_males = pd.merge(males_by_state, census_df, left_on='Rndrng_Prvdr_State_Abrvtn', right_on='State')
    merged_males['docs_per_100k'] = (merged_males['Rndrng_NPI'] / merged_males['Population in 2021']) * 100000
    merged_males = merged_males.sort_values('docs_per_100k', ascending=False)
    merged_females = pd.merge(females_by_state, census_df, left_on='Rndrng_Prvdr_State_Abrvtn', right_on='State')
    merged_females['docs_per_100k'] = (merged_females['Rndrng_NPI'] / merged_females['Population in 2021']) * 100000
    merged_females = merged_females.sort_values('docs_per_100k', ascending=False)

    # Find the number of male physicians per 100,000 people by state
    merged_males.columns = [col + '_male' for col in merged_males.columns]
    merged_females.columns = [col + '_female' for col in merged_females.columns]
    merged_data = pd.merge(merged_males, merged_females, left_on='State_male', right_on='State_female')
    merged_data['male_percent'] = merged_data['Rndrng_NPI_male'] / (merged_data['Rndrng_NPI_female'] + merged_data['Rndrng_NPI_male'])*100
    merged_data['female_percent'] = merged_data['Rndrng_NPI_female'] / (merged_data['Rndrng_NPI_female'] + merged_data['Rndrng_NPI_male'])*100
    merged_data_sorted = merged_data.sort_values('female_percent', ascending=False)

    # Create a bar plot of the top 5 and bottom 5 states by percentage female physicians
    top_bottom_5 = merged_data_sorted.head(5)._append(merged_data_sorted.tail(5))

    # Create a new column for the x-coordinates
    top_bottom_5['x'] = range(10)

    # Add a gap in the middle
    top_bottom_5.loc[top_bottom_5.index[5:], 'x'] += 1

    # Update the colors list to contain only 'steelblue'
    colors = ['steelblue'] * 10 

    # Create the bar plot
    plt.bar(top_bottom_5['x'], top_bottom_5['female_percent'], color=colors)
    plt.bar(top_bottom_5['x'], 100 - top_bottom_5['female_percent'], bottom=top_bottom_5['female_percent'], color='lightskyblue')

    # Set the x-ticks and x-tick labels
    plt.xticks(top_bottom_5['x'], top_bottom_5['State_female'], rotation=45)

    # Set the labels and title
    plt.xlabel('State')
    plt.ylabel('Percentage')
    plt.title('Figure 1. Top 5 and Bottom 5 States by Percentage Female Dermatologists')

    # Create the legend
    plt.legend(['Female', 'Male'])

    # Show the plot
    plt.show()

# Create a heat map of the percentage of female physicians by state
def create_heat_map(data):

    # Separate the data by male and female
    male_data = data[data['Rndrng_Prvdr_Gndr'] == 'M']
    female_data = data[data['Rndrng_Prvdr_Gndr'] == 'F']

    # Calculate the percentage of female physicians by state
    percent_female = (female_data.groupby('Rndrng_Prvdr_State_Abrvtn').size() / (male_data.groupby('Rndrng_Prvdr_State_Abrvtn').size() + female_data.groupby('Rndrng_Prvdr_State_Abrvtn').size())) * 100
    percent_female_df = percent_female.to_frame('percent_female')

    # Load US states shapefile
    us_states = gpd.read_file("shapefiles/cb_2018_us_state_500k.shp")

    # Merge data with the shapefile
    us_states = us_states.merge(percent_female_df, how='left', left_on='STUSPS', right_on='Rndrng_Prvdr_State_Abrvtn')
    
    # Create main plot for continental US
    fig, ax = plt.subplots(1, 1, figsize=(20, 10))
    us_states[~us_states['STUSPS'].isin(['HI', 'AK', 'PR', 'VI', 'GU', 'MP', 'AS'])].plot(
    column='percent_female', 
    cmap='Blues', 
    linewidth=0.8, 
    ax=ax, 
    edgecolor='0.8', 
    legend=True, 
    legend_kwds={'label': 'Percentage'}
    )
    ax.set_title('Figure 3. Percentage Female Dermatologists by State in 2021', fontsize=14, fontweight='normal') 

    # Create inset for Alaska
    ax_ak = fig.add_axes([0.0, -0.25, 1, 1])  # position and size of the inset (left, bottom, width, height)
    us_states[us_states['STUSPS'] == 'AK'].plot(column='percent_female', linewidth=0.8, ax=ax_ak, edgecolor='0.8', color = (88/255, 164/255, 204/255))  # custom color for Alaska

    # Create inset for Hawaii
    ax_hi = fig.add_axes([-0.15, 0.1, 0.5, 0.5])  # position and size of the inset (left, bottom, width, height)
    us_states[us_states['STUSPS'] == 'HI'].plot(column='percent_female', linewidth=0.8, ax=ax_hi, edgecolor='0.8', color = (88/255, 164/255, 204/255))  # custom color for Hawaii

    ax.axis('off')
    ax_ak.axis('off')
    ax_hi.axis('off')
    
    plt.show()


derm_data = extract_data('data/dermatolgy')
male, female, total = sort_data_by_gender(derm_data)
data_2021 = filter_data_by_year(derm_data, 2021)
data_2013 = filter_data_by_year(derm_data, 2013)
create_pie_charts(derm_data)
create_gender_comp_line_graph(male, female)
create_line_graph_total_physicians(total)
create_stacked_barchart(derm_data)
create_heat_map(data_2021)