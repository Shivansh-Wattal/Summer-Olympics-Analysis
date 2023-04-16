import numpy as np
import pandas as pd

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                             ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)
    medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
    medal_tally['Total'] = medal_tally['Total'].astype(int)

    return medal_tally

def country_year_list(df):
    Year = df['Year'].unique().tolist()
    Year.sort()
    Year.insert(0, 'Overall')

    Country = np.unique(df['region'].dropna().values).tolist()
    Country.sort()
    Country.insert(0, 'Overall')

    return Year,Country


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]

    if flag == 0:
        final_df = temp_df.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                          ascending=False).reset_index()
    if flag == 1:
        final_df = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()

    final_df['Total'] = final_df['Gold'] + final_df['Silver'] + final_df['Bronze']
    final_df['Gold'] = final_df['Gold'].astype(int)
    final_df['Silver'] = final_df['Silver'].astype(int)
    final_df['Bronze'] = final_df['Bronze'].astype(int)
    final_df['Total'] = final_df['Total'].astype(int)

    return final_df

def data_over_time(df,col):
    nations_per_edition = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values(
        'index')
    nations_per_edition.rename(columns={'index': 'Year', 'Year': col}, inplace=True)
    return (nations_per_edition)


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(20).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x


def year_wise_medals(df,country):
    tdf = df.dropna(subset=['Medal'])
    tdf.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = tdf[tdf['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_sport_pt(df,country):
    tdf = df.dropna(subset=['Medal'])
    tdf.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = tdf[tdf['region'] == country]

    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype(int)

    return pt


def most_successful_per_country(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def men_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[ athlete_df['Sex']=='M' ].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women,on='Year',how='left')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    final.fillna(0,inplace=True)

    return final


def men_women_medals(df, country):
    cdf = df[df['region'] == country]
    cdf = cdf.dropna(subset=['Medal'])
    cdf = cdf.drop_duplicates(subset=['Year', 'Sport', 'Event', 'Medal'])

    men = cdf[cdf['Sex'] == 'M'].groupby('Year').count()['Medal'].reset_index()
    women = cdf[cdf['Sex'] == 'F'].groupby('Year').count()['Medal'].reset_index()

    year_list = pd.DataFrame(df['Year'].unique().tolist())
    year_list = year_list.rename(columns={0: 'Year'})

    women_medal = year_list.merge(women, on='Year', how='left')
    women_medal['Medal'] = women_medal['Medal'].fillna(0).astype(int)
    women_medal = women_medal.sort_values('Year')

    men_medal = year_list.merge(men, on='Year', how='left')
    men_medal['Medal'] = men_medal['Medal'].fillna(0).astype(int)
    men_medal = men_medal.sort_values('Year')

    final = men_medal.merge(women_medal, on='Year')
    final = final.rename(columns={'Medal_x': 'Male', 'Medal_y': 'Female'})

    return final
