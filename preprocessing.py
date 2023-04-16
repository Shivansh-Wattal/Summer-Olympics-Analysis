import pandas as pd


def preprocess(df,region_df):
    # filter for only summer data
    df = df[df['Season'] == 'Summer']
    # left join to get region
    df = df.merge(region_df, on='NOC', how='left')
    # drop duplicates
    df.drop_duplicates(inplace=True)
    # concat to get seperate gold, silver and bronze columns
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df