#Downloading the Data
import os
import streamlit as st
import folium
from folium.plugins import FastMarkerCluster
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import folium
from folium import plugins
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

data_filename = 'US_Accidents_Dec21_updated.pkl'

def load_data():
    # Check if the pickle file exists
    if os.path.exists(data_filename):
        # Load data from pickle file if it exists
        return pd.read_pickle(data_filename)
    else:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv('US_Accidents_Dec21_updated.csv')
        
        # Convert the DataFrame to a pickle file
        df.to_pickle(data_filename)
        
        return df

#@st.cache(allow_output_mutation=True)
def load_cached_data():
    df = load_data()
    return df

df = load_cached_data()

#Outline of the Project
st.title("Analysis of US Accidents")
"""

This project presents a comprehensive analysis of car accidents in the United States using a real-world dataset. Our analysis will uncover valuable insights into the frequency and distribution of accidents across the country, and provide potential explanations for the underlying causes. The goal of this project is to contribute to efforts to reduce accidents and improve road safety by shedding light on the importance of safe driving.
"""

st.header("About the Dataset")
"""

I would like to draw your attention to a comprehensive dataset on car accidents in the United States, encompassing 49 states. The data, spanning from February 2016 to December 2021, was sourced through multiple APIs, providing real-time information on traffic incidents. These APIs transmit traffic data gathered from a range of sources, including departments of transportation at the state and federal levels, law enforcement agencies, traffic cameras, and sensors embedded within the road networks. With approximately **2.8 million records**, this dataset represents a valuable resource for those seeking to gain insights into the patterns and trends of car accidents in the US.
"""


st.subheader("Features and Attributes of the Dataset")

data = [    ['ID', 'This is a unique identifier of the accident record.'],
    ['Severity', 'Shows the severity of the accident, a number between 1 and 4, where 1 indicates the least impact on traffic (i.e., short delay as a result of the accident) and 4 indicates a significant impact on traffic (i.e., long delay).'],
    ['Start_Time', 'Shows start time of the accident in local time zone.'],
    ['End_Time', 'Shows end time of the accident in local time zone. End time here refers to when the impact of accident on traffic flow was dismissed.'],
    ['Start_Lat', 'Shows latitude in GPS coordinate of the start point.'],
    ['Start_Lng', 'Shows longitude in GPS coordinate of the start point.'],
    ['End_Lat', 'Shows latitude in GPS coordinate of the end point.'],
    ['End_Lng', 'Shows longitude in GPS coordinate of the end point.'],
    ['Distance(mi)', 'The length of the road extent affected by the accident.'],
    ['Description', 'Shows a human provided description of the accident.'],
    ['Number', 'Shows the street number in address field.'],
    ['Street', 'Shows the street name in address field.'],
    ['Side', 'Shows the relative side of the street (Right/Left) in address field.'],
    ['City', 'Shows the city in address field.'],
    ['County', 'Shows the county in address field.'],
    ['State', 'Shows the state in address field.'],
    ['Zipcode', 'Shows the zipcode in address field.'],
    ['Country', 'Shows the country in address field.'],
    ['Timezone', 'Shows timezone based on the location of the accident (eastern, central, etc.).'],
    ['Airport_Code', 'Denotes an airport-based weather station which is the closest one to location of the accident.'],
    ['Weather_Timestamp', 'Shows the time-stamp of weather observation record (in local time).'],
    ['Temperature(F)', 'Shows the temperature (in Fahrenheit).'],
    ['Wind_Chill(F)', 'Shows the wind chill (in Fahrenheit).'],
    ['Humidity(%)', 'Shows the humidity (in percentage).'],
    ['Pressure(in)', 'Shows the air pressure (in inches).'],
    ['Visibility(mi)', 'Shows visibility (in miles).'],
    ['Wind_Direction', 'Shows wind direction.'],
    ['Wind_Speed(mph)', 'Shows wind speed (in miles per hour).'],
    ['Precipitation(in)', 'Shows precipitation amount in inches, if there is any.'],
    ['Weather_Condition', 'Shows the weather condition (rain, snow, thunderstorm, fog, etc.)'],
    ['Amenity', 'A POI annotation which indicates presence of amenity in a nearby location.'],
    ['Bump', 'A POI annotation which indicates presence of speed bump or hump in a nearby location.'],
    ['Crossing', 'A POI annotation which indicates presence of crossing in a nearby location.'],
    ['Give_Way', 'A POI annotation which indicates presence of give_way in a nearby location.'],
    ['Junction', 'A POI annotation which indicates presence of junction in a nearby location.'],
    ['No_Exit', 'A POI annotation which indicates presence of no_exit in a nearby location.'],
    ['Railway', 'A POI annotation which indicates presence of railway in a nearby location.'],
    ['Roundabout', 'A POI annotation which indicates presence of roundabout in a nearby location.'],
    ['Station', 'A POI annotation which indicates presence of station in a nearby location.'],
    ['Stop', 'A POI annotation which indicates presence of stop in a nearby location.'],
    ['Traffic_Calming', 'A POI annotation which indicates presence of traffic_calming in a nearby location.'],
    ['Traffic_Signal', 'A POI annotation which indicates presence of traffic_signal in a nearby location.'],
    ['Turning_Loop', 'A POI annotation which indicates presence of turning_loop in a nearby location.'],
    ['Sunrise_Sunset', 'Shows the period of day (i.e. day or night) based on sunrise/sunset.'],
    ['Civil_Twilight', 'Shows the period of day (i.e. day or night) based on civil twilight.'],
    ['Nautical_Twilight', 'Shows the period of day (i.e. day or night) based on nautical twilight.'],
    ['Astronomical_Twilight', 'Shows the period of day (i.e. day or night) based on astronomical twilight.']
            ]
df2 = pd.DataFrame(data)

# change column names
df2.rename(columns={0: 'Attributes', 1: 'Description'}, inplace=True)

st.write(df2, table=True, index=False)
st.write("*To view longer sentences, double click on the table cell*.")


col1, col2 = st.columns([1, 1])

col1.markdown("## Number of Records")
col1.markdown("# ~ 2.8 Million")

col2.markdown("## Number of Features")
col2.markdown("# 47")



st.header("Data Preparation and Cleaning")
"""

The data preparation and cleaning phase involved loading and downloading the files using Pandas, analyzing the information contained within, and correcting or accounting for any missing or incorrect values. This step is crucial in ensuring the accuracy and reliability of our analysis.
"""
st.subheader("Percentage of Missing Values per Column")

# calculate missing values percentage
missing_percentages = df.isna().sum().sort_values(ascending=False) / len(df)

# convert to percentage
missing_percentages *= 100

# filter out columns with no missing values
filtered_missing_percentages = missing_percentages[missing_percentages > 1]

# display bar chart
st.bar_chart(filtered_missing_percentages)

st.write("Based on the bar chart of missing values, it appears that a few columns have a missing value percentage exceeding 30%. In the interest of maintaining the accuracy and representativeness of our data, it would be appropriate to exclude these columns from our analysis.")






st.header("Exploratory Analysis and Visualization")
"""

The exploratory analysis and visualization phase involved analyzing key columns such as City, Start Time, Start Latitude, and Start Longitude. These columns were chosen as they are likely to provide useful insights into the frequency and distribution of accidents across different regions and time periods. The results of this phase will be used to guide further analysis and hypothesis testing.
"""

st.subheader("Cities with the most Accidents")

cities = df.City.unique()
st.write("*The number of cities in this dataset is*: ", len(cities), " *out of over 108,000 in the United States*.")

cities_by_accident = df.City.value_counts().rename_axis('City').reset_index(name='Accidents')
st.write("Top 10 cities in the US with the most accidents")
st.write(cities_by_accident[:10])

st.write("It is noted that New York City, which is the most populated city in the United States, is not represented in this data set.")

high_accident_cities = cities_by_accident[cities_by_accident['Accidents'] >= 1000]
low_accident_cities = cities_by_accident[cities_by_accident['Accidents'] < 1000]

st.subheader("Number of Accidents per City")
st.bar_chart(cities_by_accident[:11], x='City', y='Accidents')





st.subheader("Heatmap of US Accident Incidents")
st.write("Higher Layers Represent Increased Accident Density and Severity")
#@st.cache()
def fill_df_na(df):
    return df.fillna(df.mean(axis=1))

df = fill_df_na(df)

def display_map(df, start_lat, start_lng):

    #df = df[(df['Start_Lat'] > start_lat) & (df['Start_Lng'] > start_lng)]
    
    n = min(df.shape[0], 1000)
    df = df.sample(50000)
    df1 = pd.DataFrame({'lat':df['Start_Lat'],'lon':df['Start_Lng']})
    #st.map(df1)

    st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=37.76,
        longitude=-97.4,
        zoom=3.2,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=df1,
           get_position='[lon, lat]',
           radius=20000,
           elevation_scale=40,
           elevation_range=[0, 10000],
           pickable=True,
           extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=df1,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))


st.write(display_map(df, 38.0, -95.5))

st.write("The map was generated from sampling 50,000 coordinates from the US accidents dataset and provides a visual representation of the distribution of accidents across the US. The map uses red hexagon layers to represent the density of accidents, with higher positioned layers indicating a higher number of accidents, as well as more severe ones. This map allows us to quickly identify areas with a high concentration of accidents, and can be used as a tool to help focus on reducing accidents in these areas.")





df.Start_Time = pd.to_datetime(df.Start_Time)

weekday_df = df[df.Start_Time.dt.dayofweek < 5]
weekend_df = df[df.Start_Time.dt.dayofweek >= 5]

weekday_hist = np.histogram(weekday_df.Start_Time.dt.hour, bins=24, range=(0,24))[0]
weekend_hist = np.histogram(weekend_df.Start_Time.dt.hour, bins=24, range=(0,24))[0]

st.subheader("Weekday Accidents by Hour")
weekday_choice = st.selectbox("Select a weekday", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Weekdays'])
#@st.cache
def weekday_hist_selected():
    if weekday_choice == 'Monday':
        return weekday_df[weekday_df.Start_Time.dt.dayofweek == 0].Start_Time.dt.hour.value_counts().sort_index()
    elif weekday_choice == 'Tuesday':
        return weekday_df[weekday_df.Start_Time.dt.dayofweek == 1].Start_Time.dt.hour.value_counts().sort_index()
    elif weekday_choice == 'Wednesday':
        return weekday_df[weekday_df.Start_Time.dt.dayofweek == 2].Start_Time.dt.hour.value_counts().sort_index()
    elif weekday_choice == 'Thursday':
        return weekday_df[weekday_df.Start_Time.dt.dayofweek == 3].Start_Time.dt.hour.value_counts().sort_index()
    elif weekday_choice == 'Friday':
        return weekday_df[weekday_df.Start_Time.dt.dayofweek == 4].Start_Time.dt.hour.value_counts().sort_index()
    else:
        return weekday_hist

selected_weekday_hist = weekday_hist_selected()
st.bar_chart(selected_weekday_hist, x=range(24))
st.write("Our analysis suggests that a significant proportion of accidents occur during the morning rush hour between 6am and 9am on weekdays. This is likely due to a higher volume of individuals in a hurry to arrive at their workplace. A higher peak in accidents is observed between 2pm and 5pm, which corresponds to the evening commute as individuals leave work and return home.")

st.subheader("Weekend Accidents by Hour")
weekend_choice = st.selectbox("Select a weekend day", ['Saturday', 'Sunday', 'Weekend Days'])
#@st.cache
def weekend_hist_selected():
     if weekend_choice == 'Saturday':
        return weekend_df[weekend_df.Start_Time.dt.dayofweek == 5].Start_Time.dt.hour.value_counts().sort_index()
     elif weekend_choice == 'Sunday':
        return weekend_df[weekend_df.Start_Time.dt.dayofweek == 6].Start_Time.dt.hour.value_counts().sort_index()
     else:
        return weekend_hist
        
selected_weekdend_hist = weekend_hist_selected()
st.bar_chart(weekend_hist_selected(), x=range(24))
st.write("Our analysis shows that there is a relatively consistent frequency of accidents occurring throughout the day on weekends, with a noticeable increase in accident occurrences observed between 11am and 6pm.")






st.header("Key Takeaways and Observations")
"""

Several key observations were made during the analysis of the US Accidents dataset. Excluding columns with over 30% missing values is recommended to ensure the data's accuracy and representativeness. Additionally, the absence of New York City, the most populous city in the United States, in the dataset may impact the overall representation of accidents in the country.

The analysis revealed a higher frequency of accidents during rush hour periods, with a significant proportion of accidents occurring during the morning and evening commutes. On weekends, a relatively consistent frequency of accidents was observed throughout the day, with a noticeable increase in occurrences between 11am and 6pm. However, the dataset did not include important factors that may contribute to car accidents, such as demographic factors, accident history, criminal record, sobriety, car body style, and car condition. Analyzing these factors may help identify potential solutions to reduce accident rates.

To decrease accident rates in the United States, it is essential to consider various factors that may contribute to car accidents. Unfortunately, the analysis was limited by the dataset, which did not include some essential factors. Therefore, it may be useful to investigate demographic factors such as age, nationality, and gender in car accidents. Other relevant information, including the driver's accident history, whether they are a first-time or repeat offender, and their existing criminal record, should be considered. It may also be helpful to investigate the role of sobriety and car body style, including micro, sedan, CUV, SUV, and others. Additionally, it may be useful to consider car condition, specifically whether the car is registered and insured. Analyzing these factors may help us better understand the causes of car accidents and identify potential solutions to reduce accident rates.
"""



