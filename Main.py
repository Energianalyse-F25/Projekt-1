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
# find mean sport price of each year
DK2_df_hour_year = DK2_df.groupby(['Year','HourOfDay']).agg({'SpotPriceDKK': 'mean'}).reset_index()

# plot for 2019
DK2_df_hour_year["mean_prices_2019"]= DK2_df_hour_year.loc[DK2_df_hour_year["Year"] == "2019"].values

print(DK2_df_hour_year)


