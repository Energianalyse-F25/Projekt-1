import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import os
import cvxpy as cp

##### Load data #####
price_path = os.path.join(os.getcwd(),'Data/ElspotpricesEA.csv')
df_prices = pd.read_csv(price_path)

#Convert to datetime
df_prices["HourDK"] = pd.to_datetime(df_prices["HourDK"])
df_prices["HourUTC"] = pd.to_datetime(df_prices["HourUTC"])
df_prices['HourUTC'] = df_prices['HourUTC'].dt.tz_localize('UTC')
df_prices['HourDK'] = df_prices['HourUTC'].dt.tz_convert('CET')

#Retrieve DK2 only
DK2_df = df_prices.loc[df_prices["PriceArea"] == "DK2"]

#keep the time and price columns
DK2_df = DK2_df[["HourDK", "SpotPriceDKK"]] #, "HourUTC"

#Retrieve only from 2019-2023 
DK2_df = DK2_df.loc[df_prices["HourDK"].dt.year.isin([2019,2020,2021,2022,2023])]
DK2_df = DK2_df.reset_index(drop=True)

### Add more columns to DK2_df to indicate the month, year, day of month and day of year ###
DK2_df["Month"] = DK2_df["HourDK"].dt.month
DK2_df["Year"] = DK2_df["HourDK"].dt.year
DK2_df["DayOfMonth"] = DK2_df["HourDK"].dt.day
DK2_df["DayOfYear"] = DK2_df["HourDK"].dt.dayofyear
DK2_df["HourOfDay"] = DK2_df["HourDK"].dt.hour



###### Task 1.1 ######

# find mean sport price of each year
DK2_df_year = DK2_df.groupby('Year').agg({'SpotPriceDKK': 'mean'}).reset_index()

plt.figure(figsize=(6, 4))
plt.bar(DK2_df_year["Year"], DK2_df_year["SpotPriceDKK"])
plt.xlabel("Year")
plt.ylabel("Average spot price (DKK/MWh)")
plt.title("Average yearly spot prices time-series 2019-2023")
plt.grid(alpha=0.25)
plt.tight_layout()
#plt.show()


###### Task 1.1 ######
# find mean spot price of each year
DK2_df_hour_year = DK2_df.groupby(['Year','HourOfDay']).agg({'SpotPriceDKK': 'mean'}).reset_index()

"""# mean spot price for 2019
mean_prices_2019 = DK2_df_hour_year.loc[(DK2_df_hour_year["Year"] == 2019), "SpotPriceDKK"].values

# initiate subplots
fig, axs = plt.subplots(2,3)

# plot for 2019
axs[0,0].bar(list(range(1,25)), mean_prices_2019)
axs[0,0].set_xlabel("Hour of day")
axs[0,0].set_ylabel("Average spot price (DKK/MWh)")
axs[0,0].set_title("Average hourly spot prices in 2019")
axs[0,0].grid(alpha=0.25)
#axs[0,0].set_tightlayout()

# mean spot price for 2020
mean_prices_2020 = DK2_df_hour_year.loc[(DK2_df_hour_year["Year"] == 2020), "SpotPriceDKK"].values

# plot for 2019
axs[0,1].figure(figsize=(10, 6))
axs[0,1].subplot()
axs[0,1].bar(list(range(1,25)), mean_prices_2020)
axs[0,1].set_xlabel("Hour of day")
axs[0,1].set_ylabel("Average spot price (DKK/MWh)")
axs[0,1].set_title("Average hourly spot prices in 2020")
axs[0,1].grid(alpha=0.25)
#axs[0,1].set_tightlayout()



plt.show()"""


# Defines the years we want to plot
years_to_plot = [2019, 2020, 2021, 2022, 2023]

# Creates a figure with 2 rows and 3 columns
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(10, 5))
axs = axs.flatten()  # Flatten the array for easy iteration

# for-loop over the years and corresponding subplot axes
for i, year in enumerate(years_to_plot):
    mean_prices = DK2_df_hour_year.loc[DK2_df_hour_year["Year"] == year, "SpotPriceDKK"].values # filters dataframe and gets the mean spotprice based on year
    axs[i].bar(range(1, 25), mean_prices)
    axs[i].set_xlabel("Hour of day")
    axs[i].set_ylabel("Average spot price (DKK/MWh)")
    axs[i].set_title(f"Average hourly prices in {year}")
    axs[i].grid(alpha=0.25)

# the 2x3 grid provides 6 plots but we only have 5 years so we have to hide the last unused subpot
#if len(years_to_plot) < len(axs):
axs[-1].set_visible(False)

plt.tight_layout()
plt.show()


