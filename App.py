import streamlit as st
import pandas as pd
import preprocessing,helper
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt
import scipy



df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessing.preprocess(df,region_df)

st.sidebar.title('Olympics Analysis')
st.sidebar.image('1619625177_olympics-1-1024x576.jpg')
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis')
)



if user_menu == 'Medal Tally':
    st.sidebar.header('Medal_Tally')
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country',country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Medal Tally of '+selected_country)
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in '+str(selected_year))
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title('Medal Tally of '+selected_country+' in the year '+str(selected_year))

    st.table(medal_tally)



if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    countries = df['region'].unique().shape[0]

    st.title('Top Numbers')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Host Cities')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1,col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(athletes)
    with col3:
        st.header('Countries')
        st.title(countries)

    nations_per_edition = helper.data_over_time(df,'region')
    fig = px.line(nations_per_edition, x='Year', y='region')
    st.title('Participating Nations')
    st.plotly_chart(fig)

    events_per_edition = helper.data_over_time(df, 'Event')
    fig = px.line(events_per_edition, x='Year', y='Event')
    st.title('No of events')
    st.plotly_chart(fig)

    athletes_per_edition = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_per_edition, x='Year', y='Name')
    st.title('No of athletes')
    st.plotly_chart(fig)

    st.title('Men v/s Women participation')
    final = helper.men_women(df)
    fig = px.line(final,x='Year',y=['Male','Female'])
    st.plotly_chart(fig)

    st.title('No of events over time ( All sports)')
    fig,ax = plt.subplots(figsize=(20,20))
    temp_df = df.drop_duplicates(['Year', 'Event', 'Sport'])
    ax = sns.heatmap(
        temp_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
        annot=True)
    st.pyplot(fig)

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    a1 = athlete_df['Age'].dropna()
    a2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    a3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    a4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([a1, a2, a3, a4], ['General', 'Gold medallist', 'Silver medallist', 'Bronze medallist'],
                             show_hist=False, show_rug=False)
    st.title('Distribution of age of athletes')
    st.plotly_chart(fig)

    st.title('Most successful athletes')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a sport',sports_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)



if user_menu == 'Country-Wise Analysis':

    st.sidebar.title('Country-Wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a country',country_list)

    country_df = helper.year_wise_medals(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title('Medal Tally of '+selected_country)
    st.plotly_chart(fig)

    medal_df =helper.men_women_medals(df,selected_country)
    fig = px.line(medal_df, x='Year', y=['Male','Female'])
    st.title('Men v/s Women medal tally of '+ selected_country)
    st.plotly_chart(fig)

    st.title(selected_country+' over the years')
    pt =  helper.country_sport_pt(df,selected_country)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title('Top 15 athletes of '+selected_country)
    top_df = helper.most_successful_per_country(df,selected_country)
    st.table(top_df)





