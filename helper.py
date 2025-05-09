import numpy as np

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
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x
def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'region', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                ascending=False).reset_index()

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')

    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def data_over_time(df,col):

    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    nations_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)

    return nations_over_time


def most_successful(df, sport):
    # Remove rows where 'Medal' is NaN (i.e., athletes who didn't win any medal)
    temp_df = df.dropna(subset=['Medal'])

    # If a specific sport is selected, filter by that sport
    if sport != "Overall":
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count medals per athlete
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']  # Rename the columns for clarity

    # Merge with original dataset to get 'Sport' and 'region' details
    x = medal_counts.head(15).merge(df[['Name', 'Sport', 'region']], on='Name', how='left').drop_duplicates('Name')

    return x

def yearwise_medal_tally(df,country):

    country_df = df.dropna(subset=['Medal'])

    country_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = country_df[country_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_event_heatmap(df,country):

    country_df = df.dropna(subset=['Medal'])

    country_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = country_df[country_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    return pt


def most_successful_countrywise(df, country):
    # Filter the dataframe to keep only rows with medals and the selected country
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    # Get the top 15 athletes by medal count
    value_counts_df = temp_df['Name'].value_counts().reset_index()
    value_counts_df.columns = ['Name', 'Medals']  # Rename columns

    # Merge with the original dataframe to get additional information (like 'Sport')
    merged_df = value_counts_df.head(10).merge(df, on='Name', how='left')[['Name', 'Medals', 'Sport']].drop_duplicates('Name')

    return merged_df


def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'City'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
       temp_df = athlete_df[athlete_df['Sport'] == sport]
       return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'City'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final










