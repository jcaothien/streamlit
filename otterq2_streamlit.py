import pandas as pd
import streamlit as st
import datetime
import plotly.express as px

st.set_page_config(page_title='Otter Restaurant Product Analytics Dashboard', page_icon=":bar_chart:", layout="wide")
st.sidebar.header('Product Dashboard')

# --- LOAD DATAFRAME
csv_file = 'transformed data - includes adoption, stickiness, and revenue.csv'

df = pd.read_csv(r'c:\Users\5\AppData\Local\Programs\Python\Python311\projects\Otter Scratch Work\Question 2\transformed data - includes adoption, stickiness, and revenue.csv')

df['day_partition'] = pd.to_datetime(df['day_partition']).dt.date
def convert_df(df):
    return df.to_csv()
downloadable_csv = convert_df(df)

# --- SIDEBAR ---

st.sidebar.header("Please Filter Here:")

Country = st.sidebar.multiselect(
    "Select the Country:",
    options=df["country"].unique(),
    default=df["country"].unique()
)
Region = st.sidebar.multiselect(
    "Select the Region:",
    options=df["region"].unique(),
    default=df["region"].unique()
)

st.sidebar.header("Date range")

min_date = datetime.datetime(2022, 1, 1)
max_date = datetime.datetime(2023, 6, 11)

selected_date_range = st.sidebar.date_input("Pick a date", value=(min_date, max_date))

# Extract the selected min and max dates
min_date, max_date = selected_date_range

# Filter the DataFrame using datetime.datetime objects for comparison
df_selection = df.query(
    "country == @Country & region == @Region & day_partition >= @min_date & day_partition <= @max_date"
)

st.sidebar.markdown('''
---
Created by [Jeremy Caothien](https://www.linkedin.com/in/jeremy-caothien-334aa3a4/).
''')

# ---- MAINPAGE ----
st.title("Overall Metrics")
total_revenue = int(df_selection["overall_revenue"].sum())
median_overall_monthly_adoption_percentage = round(df_selection["adoption_monthly_overall"].median(), 2)
median_stickiness_overall = round(df_selection["stickiness_overall"].median(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Revenue:")
    st.subheader(f"US $ {total_revenue:,}")
with middle_column:
    st.subheader("Median Monthly Adoption Percent:")
    st.subheader(f" {median_overall_monthly_adoption_percentage * 100} %")
with right_column:
    st.subheader("Median Stickiness Percentage:")
    st.subheader(f" {median_stickiness_overall * 100} %")

st.markdown("---")

# --- DATA ---
st.header('Data')
st.subheader(
    'Transformed data. This includes adoption, stickiness, and revenue. Duplicate country rows per date are aggregated.')
st.dataframe(df_selection)
st.download_button(
    label="Download the transformed data as a csv",
    data=downloadable_csv,
    file_name='transformed data - includes adoption, stickiness, and revenue.csv',
    mime='text/csv'
)

# --- ADOPTION ---
st.header('Adoption')
st.markdown("---")
st.markdown("The insights for Product adoption are organized below. Adoption is defined as the ratio of Active/Access. This is done both at the daily level and monthly level.")

st.subheader('General - Overall, Core, Premium')

# Group the data by 'region' and calculate the mean of adoption columns
df_grouped = df_selection.groupby(['day_partition', 'region'])[['adoption_daily_overall', 'adoption_daily_core', 'adoption_daily_premium']].mean().reset_index()

# Create the line chart
overall_daily_adoption = px.line(
    df_grouped, 
    x='day_partition', 
    y=['adoption_daily_overall'], 
    color='region',  # Color lines by region
    title='Overall Daily Adoption'
)

core_daily_adoption = px.line(
    df_grouped, 
    x='day_partition', 
    y=['adoption_daily_core'], 
    color='region',  # Color lines by region
    title='Core Daily Adoption'
)

premium_daily_adoption = px.line(
    df_grouped, 
    x='day_partition', 
    y=['adoption_daily_overall'], 
    color='region',  # Color lines by region
    title='Premium Daily Adoption'
)


# --- BUBBLE CHARTS
# Group the data by 'country' and calculate the median of 'adoption_daily_overall' for bubble sizes
df_bubble = df_selection[df_selection['day_partition'] == max_date]  # Filter data for the last date in the date range

# -- OVERALL DAILY ADOPTION
overall_daily_adoption_bubble_chart = px.scatter(
    df_bubble,
    x='locations',
    y='adoption_daily_overall',
    color='region',
    size='locations',
    hover_name='country',  # Show country names on hover
    title='Overall Adoption % by Country & Locations'
)

# Customize labels
overall_daily_adoption_bubble_chart.update_xaxes(title='Locations')
overall_daily_adoption_bubble_chart.update_yaxes(title='Average Adoption Daily Overall')
overall_daily_adoption_bubble_chart.update_traces(marker_line_color='rgba(0,0,0,0)')

# -- CORE DAILY ADOPTION
core_daily_adoption_bubble_chart = px.scatter(
    df_bubble,
    x='locations',
    y='adoption_daily_core',
    color='region',
    size='locations',
    hover_name='country',  # Show country names on hover
    title='Core Adoption % by Country & Locations'
)

# Customize labels
core_daily_adoption_bubble_chart.update_xaxes(title='Locations')
core_daily_adoption_bubble_chart.update_yaxes(title='Average Adoption Daily Core')
core_daily_adoption_bubble_chart.update_traces(marker_line_color='rgba(0,0,0,0)')

# -- PREMIUM DAILY ADOPTION
premium_daily_adoption_bubble_chart = px.scatter(
    df_bubble,
    x='locations',
    y='adoption_daily_premium',
    color='region',
    size='locations',
    hover_name='country',  # Show country names on hover
    title='Core Adoption % by Country & Locations'
)

# Customize labels
premium_daily_adoption_bubble_chart.update_xaxes(title='Locations')
premium_daily_adoption_bubble_chart.update_yaxes(title='Average Adoption Daily Premium')
premium_daily_adoption_bubble_chart.update_traces(marker_line_color='rgba(0,0,0,0)')


# Display the line charts in the first column
col1, col2 = st.columns(2)

with col1:
    st.subheader('Daily Adoption by Region')
    st.plotly_chart(overall_daily_adoption)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
    st.plotly_chart(core_daily_adoption)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
    st.plotly_chart(premium_daily_adoption)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")


# Create a bubble chart for the second column
with col2:
    st.subheader('Bubble Chart by Country')
    st.plotly_chart(overall_daily_adoption_bubble_chart)
    st.markdown(f"For the date: {max_date.strftime('%Y-%m-%d')}")
    st.plotly_chart(core_daily_adoption_bubble_chart)
    st.markdown(f"For the date: {max_date.strftime('%Y-%m-%d')}")
    st.plotly_chart(premium_daily_adoption_bubble_chart)
    st.markdown(f"For the date: {max_date.strftime('%Y-%m-%d')}")

st.markdown("---")
# --- ADOPTION - INSIGHTS & ANALYTICS FEATURES ----
st.subheader('Insights & Analytics - Basic, Advance, Super')
df_grouped = df_selection.groupby(['day_partition', 'region'])[['adoption_daily_basic_insights', 'adoption_daily_adv_insights', 'adoption_daily_super_insights']].mean().reset_index()

# Create the line chart

# --- LINE CHARTS 
basic_insights_daily_adoption_daily_adoption = px.line(
    df_grouped, 
    x='day_partition', 
    y=['adoption_daily_basic_insights'], 
    color='region',  # Color lines by region
    title='Overall Daily Adoption'
)

adv_insights_daily_adoption = px.line(
    df_grouped, 
    x='day_partition', 
    y=['adoption_daily_adv_insights'], 
    color='region',  # Color lines by region
    title='Core Daily Adoption'
)

super_insights_daily_adoption = px.line(
    df_grouped, 
    x='day_partition', 
    y=['adoption_daily_super_insights'], 
    color='region',  # Color lines by region
    title='Premium Daily Adoption'
)

# --- BUBBLE CHARTS
# Group the data by 'country' and calculate the median of 'adoption_daily_overall' for bubble sizes
df_bubble = df_selection[df_selection['day_partition'] == max_date]  # Filter data for the last date in the date range

# -- OVERALL DAILY ADOPTION
basic_insights_daily_adoption_bubble_chart = px.scatter(
    df_bubble,
    x='locations',
    y='adoption_daily_basic_insights',
    color='region',
    size='locations',
    hover_name='country',  # Show country names on hover
    title='Basic Insights Adoption % by Country & Locations'
)

# Customize labels
basic_insights_daily_adoption_bubble_chart.update_xaxes(title='Locations')
basic_insights_daily_adoption_bubble_chart.update_yaxes(title='Average Adoption Daily Basic Insights')
basic_insights_daily_adoption_bubble_chart.update_traces(marker_line_color='rgba(0,0,0,0)')

# -- ADV INSIGHTS DAILY ADOPTION
adv_insights_daily_adoption_bubble_chart = px.scatter(
    df_bubble,
    x='locations',
    y='adoption_daily_adv_insights',
    color='region',
    size='locations',
    hover_name='country',  # Show country names on hover
    title='Advance Insights Adoption % by Country & Locations'
)

# Customize labels
adv_insights_daily_adoption_bubble_chart.update_xaxes(title='Locations')
adv_insights_daily_adoption_bubble_chart.update_yaxes(title='Average Adoption Adv Insights')
adv_insights_daily_adoption_bubble_chart.update_traces(marker_line_color='rgba(0,0,0,0)')

# -- SUPER INSIGHTS DAILY ADOPTION
super_insights_daily_adoption_bubble_chart = px.scatter(
    df_bubble,
    x='locations',
    y='adoption_daily_super_insights',
    color='region',
    size='locations',
    hover_name='country',  # Show country names on hover
    title='Super Insights Adoption % by Country & Locations'
)

# Customize labels
super_insights_daily_adoption_bubble_chart.update_xaxes(title='Locations')
super_insights_daily_adoption_bubble_chart.update_yaxes(title='Average Adoption Super Insights')
super_insights_daily_adoption_bubble_chart.update_traces(marker_line_color='rgba(0,0,0,0)')

# Display the line charts in the first column
col1, col2 = st.columns(2)

with col1:
    st.subheader('Daily Adoption by Region')
    st.plotly_chart(basic_insights_daily_adoption_daily_adoption)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(adv_insights_daily_adoption)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(super_insights_daily_adoption)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")



with col2:
    st.subheader('Bubble Chart by Country')
    st.plotly_chart(basic_insights_daily_adoption_bubble_chart)
    st.markdown(f"For the date: {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(adv_insights_daily_adoption_bubble_chart)
    st.markdown(f"For the date: {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(super_insights_daily_adoption_bubble_chart)
    st.markdown(f"For the date: {max_date.strftime('%Y-%m-%d')}")


st.markdown("---")
st.subheader('Other Features - Promos & Custom Websites')

df_grouped = df_selection.groupby(['day_partition', 'region'])[['adoption_daily_custom_websites', 'adoption_daily_promos',]].mean().reset_index()

# Create the line chart

# --- LINE CHARTS 
custom_websites_daily_adoption_daily_adoption = px.line(
    df_grouped, 
    x='day_partition', 
    y=['adoption_daily_custom_websites'], 
    color='region',  # Color lines by region
    title='Custom Websites Daily Adoption'
)

promos_daily_adoption = px.line(
    df_grouped, 
    x='day_partition', 
    y=['adoption_daily_promos'], 
    color='region',  # Color lines by region
    title='Promos Daily Adoption'
)

# --- BUBBLE CHARTS
# Group the data by 'country' and calculate the median of 'adoption_daily_overall' for bubble sizes
df_bubble = df_selection[df_selection['day_partition'] == max_date]  # Filter data for the last date in the date range

# -- OVERALL DAILY ADOPTION
custom_websites_daily_adoption_bubble_chart = px.scatter(
    df_bubble,
    x='locations',
    y='adoption_daily_custom_websites',
    color='region',
    size='locations',
    hover_name='country',  # Show country names on hover
    title='Custom Websites Adoption % by Country & Locations'
)

# Customize labels
custom_websites_daily_adoption_bubble_chart.update_xaxes(title='Locations')
custom_websites_daily_adoption_bubble_chart.update_yaxes(title='Average Adoption Daily Custom Websites')
custom_websites_daily_adoption_bubble_chart.update_traces(marker_line_color='rgba(0,0,0,0)')

# -- ADV INSIGHTS DAILY ADOPTION
promos_daily_adoption_bubble_chart = px.scatter(
    df_bubble,
    x='locations',
    y='adoption_daily_promos',
    color='region',
    size='locations',
    hover_name='country',  # Show country names on hover
    title='Advance Insights Adoption % by Country & Locations'
)

# Customize labels
promos_daily_adoption_bubble_chart.update_xaxes(title='Locations')
promos_daily_adoption_bubble_chart.update_yaxes(title='Average Adoption Promos')
promos_daily_adoption_bubble_chart.update_traces(marker_line_color='rgba(0,0,0,0)')


# Display the line charts in the first column
col1, col2 = st.columns(2)

with col1:
    st.subheader('Daily Adoption by Region')
    st.plotly_chart(custom_websites_daily_adoption_daily_adoption)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(promos_daily_adoption)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")



with col2:
    st.subheader('Bubble Chart by Country')
    st.plotly_chart(custom_websites_daily_adoption_bubble_chart)
    st.markdown(f"For the date: {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(promos_daily_adoption_bubble_chart)
    st.markdown(f"For the date: {max_date.strftime('%Y-%m-%d')}")



# --- STICKINESS ---
st.header('Stickiness')
st.markdown("---")
st.markdown("The insights for Product adoption are organized below. Adoption is defined as the ratio of Daily Active/ Monthly Active. This is done both at the daily level and monthly level.")

st.subheader('General - Overall, Core, Premium')

# Group the data by 'region' and calculate the mean of adoption columns
df_grouped = df_selection.groupby(['day_partition', 'region'])[['stickiness_overall', 'stickiness_core', 'stickiness_premium','stickiness_custom_websites']].mean().reset_index()

# Create the line chart
stickiness_overall = px.line(
    df_grouped, 
    x='day_partition', 
    y=['stickiness_overall'], 
    color='region',  # Color lines by region
    title='Overall Stickiness'
)
stickiness_overall.update_yaxes(title='Stickiness %')

stickiness_core = px.line(
    df_grouped, 
    x='day_partition', 
    y=['stickiness_core'], 
    color='region',  # Color lines by region
    title='Core Stickiness'
)
stickiness_core.update_yaxes(title='Stickiness %')

stickiness_premium = px.line(
    df_grouped, 
    x='day_partition', 
    y=['stickiness_premium'], 
    color='region',  # Color lines by region
    title='Premium Stickiness'
)

stickiness_premium.update_yaxes(title='Stickiness %')

# --- BUBBLE CHARTS
# Group the data by 'country' and calculate the median of 'adoption_daily_overall' for bubble sizes
df_bubble = df_selection[df_selection['day_partition'] == max_date]  # Filter data for the last date in the date range

# -- OVERALL DAILY ADOPTION
overall_stickiness_bubble_chart = px.scatter(
    df_bubble,
    x='locations',
    y='stickiness_overall',
    color='region',
    size='locations',
    hover_name='country',  # Show country names on hover
    title='Overall Stickiness % by Country & Locations'
)

# Customize labels
overall_stickiness_bubble_chart.update_xaxes(title='Locations')
overall_stickiness_bubble_chart.update_yaxes(title='Stickiness Overall')
overall_stickiness_bubble_chart.update_traces(marker_line_color='rgba(0,0,0,0)')

# -- CORE DAILY ADOPTION
core_stickiness_bubble_chart = px.scatter(
    df_bubble,
    x='locations',
    y='stickiness_core',
    color='region',
    size='locations',
    hover_name='country',  # Show country names on hover
    title='Core Stickiness % by Country & Locations'
)

# Customize labels
overall_stickiness_bubble_chart.update_xaxes(title='Locations')
overall_stickiness_bubble_chart.update_yaxes(title='Stickiness Core')
overall_stickiness_bubble_chart.update_traces(marker_line_color='rgba(0,0,0,0)')

# -- PREMIUM DAILY ADOPTION
premium_stickiness_bubble_chart = px.scatter(
    df_bubble,
    x='locations', 
    y='stickiness_premium',
    color='region',
    size='locations',
    hover_name='country',  # Show country names on hover
    title='Premium Stickiness % by Country & Locations'
)

# Customize labels
premium_stickiness_bubble_chart.update_xaxes(title='Locations')
premium_stickiness_bubble_chart.update_yaxes(title='Stickiness Premium')
premium_stickiness_bubble_chart.update_traces(marker_line_color='rgba(0,0,0,0)')


# Display the line charts in the first column
col1, col2 = st.columns(2)

with col1:
    st.subheader('Stickiness by Region')
    st.plotly_chart(stickiness_overall)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
    st.plotly_chart(stickiness_core)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
    st.plotly_chart(stickiness_premium)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")


# Create a bubble chart for the second column
with col2:
    st.subheader('Bubble Chart by Country')
    st.plotly_chart(overall_stickiness_bubble_chart)
    st.markdown(f"For the date: {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(core_stickiness_bubble_chart)
    st.markdown(f"For the date: {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(premium_stickiness_bubble_chart)
    st.markdown(f"For the date: {max_date.strftime('%Y-%m-%d')}")

st.markdown("---")
# --- ADOPTION - INSIGHTS & ANALYTICS FEATURES ----
st.subheader('Insights & Analytics - Basic, Advance, Super')
df_grouped = df_selection.groupby(['day_partition', 'region'])[['stickiness_basic_insights', 'stickiness_adv_insights', 'stickiness_super_insights']].mean().reset_index()

# Create the line chart

# --- LINE CHARTS 
basic_insights_stickiness = px.line(
    df_grouped, 
    x='day_partition', 
    y=['stickiness_basic_insights'], 
    color='region',  # Color lines by region
    title='Basic Insights Stickiness'
)
basic_insights_stickiness.update_yaxes(title='Stickiness Basic Insights %')

adv_insights_stickiness = px.line(
    df_grouped, 
    x='day_partition', 
    y=['stickiness_adv_insights'], 
    color='region',  # Color lines by region
    title='Advanced Insights Stickiness'
)
adv_insights_stickiness.update_yaxes(title='Stickiness Advanced Insights %')

super_insights_stickiness = px.line(
    df_grouped, 
    x='day_partition', 
    y=['stickiness_super_insights'], 
    color='region',  # Color lines by region
    title='Super Insights Stickiness'
)
super_insights_stickiness.update_yaxes(title='Stickiness Super Insights %')

# --- BUBBLE CHARTS
# Group the data by 'country' and calculate the median of 'adoption_daily_overall' for bubble sizes
df_bubble = df_selection[df_selection['day_partition'] == max_date]  # Filter data for the last date in the date range

# -- OVERALL DAILY ADOPTION
basic_insights_stickiness_bubble_chart = px.scatter(
    df_bubble,
    x='locations',
    y='stickiness_basic_insights',
    color='region',
    size='locations',
    hover_name='country',  # Show country names on hover
    title='Basic Insights Stickiness % by Country & Locations'
)

# Customize labels
basic_insights_stickiness_bubble_chart.update_xaxes(title='Locations')
basic_insights_stickiness_bubble_chart.update_yaxes(title='Stickiness Basic Insights %')
basic_insights_stickiness_bubble_chart.update_traces(marker_line_color='rgba(0,0,0,0)')

# -- ADV INSIGHTS DAILY ADOPTION
adv_insights_stickiness_bubble_chart = px.scatter(
    df_bubble,
    x='locations',
    y='stickiness_adv_insights',
    color='region',
    size='locations',
    hover_name='country',  # Show country names on hover
    title='Advance Insights Stickiness % by Country & Locations'
)

# Customize labels
adv_insights_stickiness_bubble_chart.update_xaxes(title='Locations')
adv_insights_stickiness_bubble_chart.update_yaxes(title='Stickiness Adv Insights %')
adv_insights_stickiness_bubble_chart.update_traces(marker_line_color='rgba(0,0,0,0)')

# -- SUPER INSIGHTS DAILY ADOPTION
super_insights_stickiness_bubble_chart = px.scatter(
    df_bubble,
    x='locations',
    y='stickiness_super_insights',
    color='region',
    size='locations',
    hover_name='country',  # Show country names on hover
    title='Super Insights Stickiness % by Country & Locations'
)

# Customize labels
super_insights_stickiness_bubble_chart.update_xaxes(title='Locations')
super_insights_stickiness_bubble_chart.update_yaxes(title='Stickiness Super Insights %')
super_insights_stickiness_bubble_chart.update_traces(marker_line_color='rgba(0,0,0,0)')

# Display the line charts in the first column
col1, col2 = st.columns(2)

with col1:
    st.subheader('Daily Adoption by Region')
    st.plotly_chart(basic_insights_stickiness)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(adv_insights_stickiness)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(super_insights_stickiness)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")



with col2:
    st.subheader('Bubble Chart by Country')
    st.plotly_chart(basic_insights_stickiness_bubble_chart)
    st.markdown(f"For the date: {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(adv_insights_stickiness_bubble_chart)
    st.markdown(f"For the date: {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(super_insights_stickiness_bubble_chart)
    st.markdown(f"For the date: {max_date.strftime('%Y-%m-%d')}")


st.markdown("---")
st.subheader('Other Features - Promos & Custom Websites')

df_grouped = df_selection.groupby(['day_partition', 'region'])[['stickiness_custom_websites', 'stickiness_promos',]].mean().reset_index()

# Create the line chart

# --- LINE CHARTS 
custom_websites_stickiness = px.line(
    df_grouped, 
    x='day_partition', 
    y=['stickiness_custom_websites'], 
    color='region',  # Color lines by region
    title='Custom Websites Stickiness'
)
custom_websites_stickiness.update_yaxes(title='Stickiness Custom Websites %')

promos_stickiness = px.line(
    df_grouped, 
    x='day_partition', 
    y=['stickiness_promos'], 
    color='region',  # Color lines by region
    title='Promos Stickiness'
)
promos_stickiness.update_yaxes(title='Stickiness Promos %')

# --- BUBBLE CHARTS
# Group the data by 'country' and calculate the median of 'adoption_daily_overall' for bubble sizes
df_bubble = df_selection[df_selection['day_partition'] == max_date]  # Filter data for the last date in the date range

# -- OVERALL DAILY ADOPTION
custom_websites_stickiness_bubble_chart = px.scatter(
    df_bubble,
    x='locations',
    y='adoption_daily_custom_websites',
    color='region',
    size='locations',
    hover_name='country',  # Show country names on hover
    title='Custom Websites Stickiness % by Country & Locations'
)

# Customize labels
custom_websites_stickiness_bubble_chart.update_xaxes(title='Locations')
custom_websites_stickiness_bubble_chart.update_yaxes(title='Stickiness Custom Websites %')
custom_websites_stickiness_bubble_chart.update_traces(marker_line_color='rgba(0,0,0,0)')

# -- ADV INSIGHTS DAILY ADOPTION
promos_stickiness_bubble_chart = px.scatter(
    df_bubble,
    x='locations',
    y='adoption_daily_promos',
    color='region',
    size='locations',
    hover_name='country',  # Show country names on hover
    title='Promos Stickiness  % by Country & Locations'
)

# Customize labels
promos_stickiness_bubble_chart.update_xaxes(title='Locations')
promos_stickiness_bubble_chart.update_yaxes(title='Stickiness Promos %')
promos_stickiness_bubble_chart.update_traces(marker_line_color='rgba(0,0,0,0)')


# Display the line charts in the first column
col1, col2 = st.columns(2)

with col1:
    st.subheader('Daily Adoption by Region')
    st.plotly_chart(custom_websites_stickiness)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(promos_stickiness)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")



with col2:
    st.subheader('Bubble Chart by Country')
    st.plotly_chart(custom_websites_stickiness_bubble_chart)
    st.markdown(f"For the date: {max_date.strftime('%Y-%m-%d')}")
    st.plotly_chart(promos_stickiness_bubble_chart)
    st.markdown(f"For the date: {max_date.strftime('%Y-%m-%d')}")

st.markdown("---")
# --- REVENUE ---
st.header('Revenue')
st.markdown('Revenue was treated differently for each of the products, based on the revenue table. Premium Custom Websites was excluded as it did not have a pricing model.')

st.subheader('General - Overall, Core, Premium')

# Group the data by 'region' and calculate the mean of adoption columns
df_grouped = df_selection.groupby(['day_partition', 'region'])[['overall_revenue', 'core_monthly_revenue', 'premium_monthly_revenue','premium_activation_revenue']].mean().reset_index()

# Create the line chart
revenue_overall = px.bar(
    df_grouped, 
    x='day_partition', 
    y=['overall_revenue'], 
    color='region',  # Color lines by region
    text_auto=True,
    title='Overall Revenue'
)
revenue_overall.update_yaxes(title='Revenue $$')

revenue_core = px.bar(
    df_grouped, 
    x='day_partition', 
    y=['core_monthly_revenue'], 
    color='region',  # Color lines by region
    text_auto=True,
    title='Core Revenue'
)
revenue_core.update_yaxes(title='Revenue $$')

revenue_monthly_premium = px.bar(
    df_grouped, 
    x='day_partition', 
    y=['premium_monthly_revenue'], 
    color='region',  # Color lines by region
    text_auto=True,
    title='Premium Monthly Revenue'
)

revenue_monthly_premium.update_yaxes(title='Revenue $$')

revenue_activation_premium = px.bar(
    df_grouped, 
    x='day_partition', 
    y=['premium_activation_revenue'], 
    color='region',  # Color lines by region
    text_auto=True,
    title='Premium Activation Revenue'
)

revenue_activation_premium.update_yaxes(title='Revenue $$')

# --- BUBBLE CHARTS
# Group the data by 'country' and calculate the median of 'adoption_daily_overall' for bubble sizes

# -- OVERALL DAILY ADOPTION
revenue_overall_pie_chart = px.pie(
    df_grouped,
    values='overall_revenue',
    names='region',
    title='Overall Revenue $$ by Region'
)

# Customize labels


# -- CORE DAILY ADOPTION
revenue_core_pie_chart = px.pie(
    df_grouped,
    values='core_monthly_revenue',
    names='region',
    title='Overall Revenue $$ by Region'
)

# -- PREMIUM DAILY ADOPTION
revenue_premium_pie_chart = px.pie(
    df_grouped,
    values='premium_monthly_revenue',
    names='region',
    title='Overall Revenue $$ by Region'
)

revenue_premium_activation_pie_chart = px.pie(
    df_grouped,
    values='premium_activation_revenue',
    names='region',
    title='Overall Revenue $$ by Region'
)

# Display the line charts in the first column
col1, col2 = st.columns(2)

with col1:
    st.subheader('Stickiness by Region')
    st.plotly_chart(revenue_overall)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
    st.plotly_chart(revenue_core)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
    st.plotly_chart(revenue_monthly_premium)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
    st.plotly_chart(revenue_activation_premium)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")


# Create a bubble chart for the second column
with col2:
    st.subheader('Pie Chart by Region')
    st.plotly_chart(revenue_overall_pie_chart)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")


    st.plotly_chart(revenue_core_pie_chart)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(revenue_premium_pie_chart)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(revenue_premium_activation_pie_chart)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")

st.markdown("---")
# --- ADOPTION - INSIGHTS & ANALYTICS FEATURES ----
st.subheader('Insights & Analytics - Basic, Advance, Super')
# Group the data by 'region' and calculate the mean of adoption columns
df_grouped = df_selection.groupby(['day_partition', 'region'])[['basic_insights_monthly_revenue', 'adv_insights_annual_revenue', 'super_insights_revenue',]].mean().reset_index()

# Create the line chart
basic_insights_revenue = px.bar(
    df_grouped, 
    x='day_partition', 
    y=['basic_insights_monthly_revenue'], 
    color='region',  # Color lines by region
    text_auto=True,
    title='Basic Insights Revenue'
)
basic_insights_revenue.update_yaxes(title='Revenue $$')

adv_insights_revenue = px.bar(
    df_grouped, 
    x='day_partition', 
    y=['adv_insights_annual_revenue'], 
    color='region',  # Color lines by region
    text_auto=True,
    title='Advanced Insights Revenue'
)
adv_insights_revenue.update_yaxes(title='Revenue $$')

super_insights_revenue = px.bar(
    df_grouped, 
    x='day_partition', 
    y=['super_insights_revenue'], 
    color='region',  # Color lines by region
    text_auto=True,
    title='Super Insights Revenue'
)

super_insights_revenue.update_yaxes(title='Revenue $$')

# --- BUBBLE CHARTS
# Group the data by 'country' and calculate the median of 'adoption_daily_overall' for bubble sizes

# -- OVERALL DAILY ADOPTION
basic_insights_revenue_pie_chart = px.pie(
    df_grouped,
    values='basic_insights_monthly_revenue',
    names='region',
    title='Overall Revenue $$ by Region'
)

# Customize labels


# -- CORE DAILY ADOPTION
adv_insights_revenue_pie_chart = px.pie(
    df_grouped,
    values='adv_insights_annual_revenue',
    names='region',
    title='Overall Revenue $$ by Region'
)

# -- PREMIUM DAILY ADOPTION
super_insights_revenue_pie_chart = px.pie(
    df_grouped,
    values='super_insights_revenue',
    names='region',
    title='Overall Revenue $$ by Region'
)


# Display the line charts in the first column
col1, col2 = st.columns(2)

with col1:
    st.subheader('Pie Chart by Region')
    st.plotly_chart(basic_insights_revenue)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
    st.plotly_chart(adv_insights_revenue)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
    st.plotly_chart(super_insights_revenue)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")


# Create a bubble chart for the second column
with col2:
    st.subheader('Bubble Chart by Country')
    st.plotly_chart(basic_insights_revenue_pie_chart)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")


    st.plotly_chart(adv_insights_revenue_pie_chart)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(super_insights_revenue_pie_chart)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")

st.markdown("---")
st.subheader('Other Features - Promos & Custom Websites')

df_grouped = df_selection.groupby(['day_partition', 'region'])[['custom_website_monthly_revenue', 'promos_monthly_revenue']].mean().reset_index()


# Create the line chart
revenue_custom_websites = px.bar(
    df_grouped, 
    x='day_partition', 
    y=['custom_website_monthly_revenue'], 
    color='region',  # Color lines by region
    text_auto=True,
    title='Custom Websites Revenue'
)
revenue_custom_websites.update_yaxes(title='Revenue $$')

revenue_promos = px.bar(
    df_grouped, 
    x='day_partition', 
    y=['promos_monthly_revenue'], 
    color='region',  # Color lines by region
    text_auto=True,
    title='Promos REvenue'
)
revenue_promos.update_yaxes(title='Revenue $$')



# --- BUBBLE CHARTS
# Group the data by 'country' and calculate the median of 'adoption_daily_overall' for bubble sizes

# -- OVERALL DAILY ADOPTION
custom_websites_revenue_pie_chart = px.pie(
    df_grouped,
    values='custom_website_monthly_revenue',
    names='region',
    title='Custom Websites Revenue $$ by Region'
)

# Customize labels


# -- CORE DAILY ADOPTION
promos_revenue_pie_chart = px.pie(
    df_grouped,
    values='promos_monthly_revenue',
    names='region',
    title='Promos Revenue $$ by Region'
)



# Display the line charts in the first column
col1, col2 = st.columns(2)

with col1:
    st.subheader('Revenue by Region')
    st.plotly_chart(revenue_custom_websites)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
    st.plotly_chart(revenue_promos)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")


# Create a bubble chart for the second column
with col2:
    st.subheader('Pie Chart Revenue  by Region')
    st.plotly_chart(custom_websites_revenue_pie_chart)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")

    st.plotly_chart(promos_revenue_pie_chart)
    st.markdown(f"For the date range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
