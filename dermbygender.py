import pandas as pd

file_path = r'C:\Users\19736\OneDrive\Documents\Github\Medicare_Physician_Other_Practitioners_by_Provider_2021.csv'
data = pd.read_csv(file_path)

# Now you can work with the imported data
# For example, you can print the first few rows
print(data.head())

males = data[data['Rndrng_Prvdr_Gndr'] == 'M']
females = data[data['Rndrng_Prvdr_Gndr'] == 'F']

males_unique_npi = males['Rndrng_NPI'].unique().tolist()
females_unique_npi = females['Rndrng_NPI'].unique().tolist()

print(f"Count of males_unique_npi:", len(males_unique_npi))
print(f"Count of females_unique_npi:", len(females_unique_npi))

males_avg_risk = males['Bene_Avg_Risk_Scre'].sum()
females_avg_risk = females['Bene_Avg_Risk_Scre'].sum()

print(f"Sum of Bene_Avg_Risk_Scre for males: {males_avg_risk}")
print(f"Sum of Bene_Avg_Risk_Scre for females: {females_avg_risk}")

males_avg_risk_per_npi = males_avg_risk / len(males_unique_npi)
females_avg_risk_per_npi = females_avg_risk / len(females_unique_npi)
print(f"Average risk per NPI for males: {males_avg_risk_per_npi}")
print(f"Average risk per NPI for females: {females_avg_risk_per_npi}")

races = ['Bene_Race_Wht_Cnt', 'Bene_Race_Black_Cnt', 'Bene_Race_API_Cnt', 'Bene_Race_Hspnc_Cnt', 'Bene_Race_NatInd_Cnt', 'Bene_Race_Othr_Cnt']

# Create a new DataFrame with columns 'Race', 'Gender', and 'Sum'
df = pd.DataFrame(columns=['Race', 'Gender', 'Sum'])

# Iterate over each race and gender combination
for race in races:
    for gender in ['Males', 'Females']:
        # Calculate the sum for the current race and gender
        total = race_sums[race][gender]
        
        # Append a new row to the DataFrame
        df = df._append({'Race': race, 'Gender': gender, 'Sum': total}, ignore_index=True)

# Print the DataFrame
print(df)


# Change the labels for the races in the DataFrame
df['Race'] = df['Race'].replace({
    'Bene_Race_Wht_Cnt': 'White',
    'Bene_Race_Black_Cnt': 'Black',
    'Bene_Race_API_Cnt': 'Asian/PI',
    'Bene_Race_Hspnc_Cnt': 'Hispanic',
    'Bene_Race_NatInd_Cnt': 'Native American',
    'Bene_Race_Othr_Cnt': 'Other'
})

# Calculate the total for each race
df['Total'] = df.groupby('Race')['Sum'].transform('sum')

# Calculate the percentage for each race and gender
df['Percent'] = df['Sum'] / df['Total'] * 100

# Print the updated DataFrame
print(df)

import matplotlib.pyplot as plt

# Group the DataFrame by 'Race' and 'Gender' columns
grouped_df = df.groupby(['Race', 'Gender']).sum()

# Reshape the DataFrame to have 'Race' as columns and 'Gender' as index
stacked_df = grouped_df.unstack()


# Plot the stacked bar chart with custom colors
stacked_df[['Percent']].plot(kind='bar', stacked=True, color=['steelblue', 'lightskyblue'])

# Set the title and labels
plt.title('Percentage of Patients Being Seen by Male vs Female Physicians by Race')
plt.xlabel('Patient Race')
plt.ylabel('Percentage')

# Show the legend with custom labels and colors
plt.legend(['Female Physicians', 'Male Physicians'], title='Physicians by Gender', facecolor='white')

# Show the plot
plt.show()

# Create a pie chart showing the count of males_unique_npi and females_unique_npi
labels = ['Males', 'Females']
sizes = [len(males_unique_npi), len(females_unique_npi)]
colors = ['lightskyblue', 'steelblue']

plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
plt.title('Distribution of Unique NPIs by Gender')
plt.axis('equal')

# Show the pie chart
plt.show()
