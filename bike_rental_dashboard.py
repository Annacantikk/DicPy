import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')
def create_season_rentals_df(df):
    season_rentals_df = df.groupby('season').agg({
        'cnt': 'sum'
    }).sort_values(by='cnt', ascending=False)
    return season_rentals_df

def create_month_rentals_df(df):
    month_rentals_df = df.groupby('mnth').agg({
        'cnt': 'sum'
    }).sort_values(by='cnt', ascending=False)
    return month_rentals_df

def create_Weekday_df(df):
    Weekday_df = df.groupby('weekday').agg({
        'cnt': 'sum'
    }).sort_values(by='cnt', ascending=False)
    return Weekday_df

def create_weathersit_df(df):
    weathersit_df = df.groupby('weathersit').agg({
        'cnt': 'sum'
    }).sort_values(by='cnt', ascending=False)
    return weathersit_df

def create_workingday_df(df):
    workingday_df = df.groupby('workingday').agg({
        'cnt': 'sum'
    }).sort_values(by='cnt', ascending=False)
    return workingday_df

def  create_holiday_df(df):
    holiday_df = df.groupby('holiday').agg({
        'cnt': 'sum'
    }).sort_values(by='cnt', ascending=False)
    return holiday_df

def create_yr_df(df):
    yr_df = df.groupby('yr').agg({
        'cnt': 'sum'
    }).sort_values(by='cnt', ascending=False)
    return yr_df

def create_temp_rentals_df(df):
    temp_rentals_df = df.groupby('temp').agg({
        'cnt': 'sum'
    }).sort_values(by='cnt', ascending=False)
    return temp_rentals_df


all_df = pd.read_csv('all_data.csv')

datetime_columns = ["dteday"]

for calumn in datetime_columns:
    all_df[calumn] = pd.to_datetime(all_df[calumn])
    
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo")

    # Mengambil start date & input date dari date input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
    (all_df["dteday"] <= str(end_date))]

season_rentals_df = create_season_rentals_df(main_df)
month_rentals_df = create_month_rentals_df(main_df)
Weekday_df = create_Weekday_df(main_df)
weathersit_df = create_weathersit_df(main_df)
workingday_df = create_workingday_df(main_df)
holiday_df = create_holiday_df(main_df)
yr_df = create_yr_df(main_df)
temp_rentals_df = create_temp_rentals_df(main_df)


st.header('Bike Sharing Dashboard :sparkles: by Anna Maulidita Widy Anggraena')

st.subheader('Daily Bike Rentals')

col1, col2 = st.columns(2)

with col1:
    total_rentals = main_df.cnt.sum()
    st.metric("Total Rentals", value=total_rentals)

with col2:
    total_casual_rentals = main_df.casual.sum()
    st.metric("Total Casual Rentals", value=total_casual_rentals)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    main_df["dteday"],
    main_df["cnt"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Visualization 1: Total orders by season
# Mapping numerical labels to season names
season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
all_df['season_label'] = all_df['season'].map(season_labels)
st.subheader('Total Orders by Season')
fig1, ax1 = plt.subplots()
season_rentals_df.groupby(season_labels)['cnt'].sum().plot(kind='bar', ax=ax1, color='skyblue')
ax1.set_ylabel('Total Rentals')
ax1.set_xlabel('season')
ax1.set_title('Total Orders by Season')
for p in ax1.patches:
    ax1.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='baseline')
st.pyplot(fig1)

# Visualization 2: Total orders by year
yr_labels = {0: '2011', 1: '2012'}
all_df['yr_label'] = all_df['yr'].map(yr_labels)
st.subheader('Total Orders by Year')
fig2, ax2 = plt.subplots()
yr_df.groupby(yr_labels)['cnt'].sum().plot(kind='bar', ax=ax2, color='orange')
ax2.set_ylabel('Total Rentals')
ax2.set_xlabel('Year')
ax2.set_title('Total Orders by Year')
for p in ax2.patches:
    ax2.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='baseline')
st.pyplot(fig2)

# Visualization 3: Orders on Working Days vs Holidays
working_labels = {0: 'Holiday or Weekday', 1: 'Working Day'}
all_df['workingday_label'] = all_df['workingday'].map(working_labels)
st.subheader('Orders on Working Days vs Holidays')
fig3, ax3 = plt.subplots()
workingday_df.groupby(working_labels)['cnt'].sum().plot(kind='bar', ax=ax3, color=['green', 'red'])
ax3.set_ylabel('Total Rentals')
ax3.set_xlabel('Day Type (0=Holiday, 1=Working Day)')
ax3.set_title('Orders on Working Days vs Holidays')
st.pyplot(fig3)

# Visualization 4: Orders based on Weather Situation
weather_labels = {1: 'Clear', 2: 'Mist', 3: 'Light Rain', 4: 'Heavy Rain'}
all_df['weathersit_label'] = all_df['weathersit'].map(weather_labels)
st.subheader('Orders Based on Weather Situation')
fig4, ax4 = plt.subplots()
weathersit_df.groupby(weather_labels)['cnt'].sum().plot(kind='bar', ax=ax4, color='purple')
ax4.set_ylabel('Total Rentals')
ax4.set_xlabel('Weather Situation')
ax4.set_title('Orders Based on Weather Situation')
st.pyplot(fig4)

# Visualization 5: Comparison of Casual and Registered Users Daily
st.subheader('Daily Casual vs Registered Users')
fig5, ax5 = plt.subplots()
main_df[['dteday', 'casual', 'registered']].set_index('dteday').plot(ax=ax5, linewidth=2)
ax5.set_ylabel('Number of Users')
ax5.set_xlabel('Date')
ax5.set_title('Daily Casual vs Registered Users')
st.pyplot(fig5)

# Visualization 6: Total Rentals per Month
month_labels = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
all_df['months_label'] = all_df['mnth'].map(month_labels)
st.subheader('Total Rental per Month')
fig2, ax2 = plt.subplots()
month_rentals_df.groupby(month_labels)['cnt'].sum().plot(kind='bar', ax=ax2, color='orange')
ax2.set_ylabel('Total Rentals')
ax2.set_xlabel('Month')
ax2.set_title('Total Orders by Month')
st.pyplot(fig2)

# Visualization 7: Total Rentals per Weekday
weekday_labels = {0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'}
all_df['weekday_label'] = all_df['weekday'].map(weekday_labels)
st.subheader('Total Rentals per Weekday')
fig2, ax2 = plt.subplots()
Weekday_df.groupby(weekday_labels)['cnt'].sum().plot(kind='bar', ax=ax2, color='orange')
ax2.set_ylabel('Total Rentals')
ax2.set_xlabel('Weekday')
ax2.set_title('Total Orders by Weekday')
st.pyplot(fig2)

